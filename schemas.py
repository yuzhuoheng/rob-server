from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, List, Any

class GameBase(BaseModel):
    """
    游戏基础模型
    
    Attributes:
        robots: 机器人初始位置和状态（JSON格式的字符串）
        walls: 墙信息（JSON格式的字符串）
        target: 目的地信息（JSON格式的字符串）
        limit: 限时（秒，默认180秒）
    """
    robots: str = Field(..., description="机器人初始位置和状态（JSON格式）")
    walls: str = Field(..., description="墙信息（JSON格式）")
    target: str = Field(..., description="目的地信息（JSON格式）")
    limit: int = Field(default=180, description="限时（秒）")

class GameCreate(GameBase):
    """
    创建游戏模型
    """
    pass

class GameUpdate(BaseModel):
    """
    更新游戏模型
    
    Attributes:
        robots: 可选的机器人信息更新
        walls: 可选的墙信息更新
        target: 可选的目标信息更新
        limit: 可选的限时更新
    """
    robots: Optional[str] = None
    walls: Optional[str] = None
    target: Optional[str] = None
    limit: Optional[int] = None

class GameInDB(GameBase):
    """
    数据库游戏模型
    
    Attributes:
        id: 主键ID
    """
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    """
    用户基础模型
    
    Attributes:
        avatar_url: 头像地址
        openid: 微信openid
        nickname: 用户昵称
    """
    avatar_url: str = Field(..., description="头像地址")
    openid: str = Field(..., description="微信openid")
    nickname: str = Field(..., description="用户昵称")

class UserCreate(UserBase):
    """
    创建用户模型
    """
    pass

class UserUpdate(BaseModel):
    """
    更新用户模型
    
    Attributes:
        avatar_url: 可选的头像地址更新
        nickname: 可选的用户昵称更新
    """
    avatar_url: Optional[str] = None
    nickname: Optional[str] = None

class UserInDB(UserBase):
    """
    数据库用户模型
    
    Attributes:
        id: 主键ID
    """
    id: int

    class Config:
        from_attributes = True 