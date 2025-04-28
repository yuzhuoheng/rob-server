from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

import models
import schemas
from database import get_db
from utils.wechat import WechatAPI

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# 创建WechatAPI实例
wechat_api = WechatAPI()

@router.post("/login", response_model=schemas.UserInDB)
async def login(code: str, db: Session = Depends(get_db)):
    """
    用户登录
    
    Args:
        code: 小程序登录时获取的 code
        db: 数据库会话
    
    Returns:
        UserInDB: 用户信息，包含：
        - openid: 用户唯一标识
        - nickname: 用户昵称
        - avatar_url: 头像地址
    """
    # 通过 code 获取 openid
    openid = await wechat_api.get_openid(code)
    
    # 检查用户是否存在
    db_user = db.query(models.User).filter(models.User.openid == openid).first()
    
    if db_user:
        # 用户存在，直接返回
        return db_user
    
    # 用户不存在，创建新用户
    new_user = models.User(
        openid=openid,
        nickname=wechat_api.generate_robot_name(),  # 生成机器人昵称
        avatar_url=""  # 默认空头像
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/", response_model=schemas.UserInDB)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    创建新用户
    
    Args:
        user: 用户数据
        db: 数据库会话
    
    Returns:
        UserInDB: 创建的用户对象
    
    Raises:
        HTTPException: 当用户已存在时
    """
    # 检查用户是否已存在
    db_user = db.query(models.User).filter(models.User.openid == user.openid).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # 创建新用户
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{openid}", response_model=schemas.UserInDB)
def get_user(openid: str, db: Session = Depends(get_db)):
    """
    获取用户信息
    
    Args:
        openid: 用户的openid
        db: 数据库会话
    
    Returns:
        UserInDB: 用户对象
    
    Raises:
        HTTPException: 当用户不存在时
    """
    db_user = db.query(models.User).filter(models.User.openid == openid).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{openid}", response_model=schemas.UserInDB)
def update_user(openid: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    更新用户信息
    
    Args:
        openid: 用户的openid
        user: 更新的用户数据
        db: 数据库会话
    
    Returns:
        UserInDB: 更新后的用户对象
    
    Raises:
        HTTPException: 当用户不存在时
    """
    db_user = db.query(models.User).filter(models.User.openid == openid).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user 