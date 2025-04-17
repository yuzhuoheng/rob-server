from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from models import get_db
import json

app = FastAPI(
    title="碰撞机器人 API",
    description="碰撞机器人游戏管理系统的 RESTful API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def validate_json_string(json_str: str, field_name: str) -> None:
    """
    验证JSON字符串格式
    
    Args:
        json_str: 要验证的JSON字符串
        field_name: 字段名称
    
    Raises:
        HTTPException: 当JSON格式无效时
    """
    try:
        json.loads(json_str)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON format in {field_name}"
        )

@app.post("/games/", response_model=schemas.GameInDB)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    """
    创建新游戏
    
    Args:
        game: 游戏数据
        db: 数据库会话
    
    Returns:
        GameInDB: 创建的游戏对象
    """
    # 验证JSON格式
    validate_json_string(game.robots, "robots")
    validate_json_string(game.walls, "walls")
    validate_json_string(game.target, "target")
    
    db_game = models.Game(
        robots=game.robots,
        walls=game.walls,
        target=game.target,
        limit=game.limit,
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@app.get("/games/", response_model=List[schemas.GameInDB])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    获取游戏列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的最大记录数
        db: 数据库会话
    
    Returns:
        List[GameInDB]: 游戏列表
    """
    games = db.query(models.Game).offset(skip).limit(limit).all()
    return games

@app.get("/games/{game_id}", response_model=schemas.GameInDB)
def read_game(game_id: int, db: Session = Depends(get_db)):
    """
    获取单个游戏
    
    Args:
        game_id: 游戏ID
        db: 数据库会话
    
    Returns:
        GameInDB: 游戏对象
    
    Raises:
        HTTPException: 当游戏不存在时
    """
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@app.put("/games/{game_id}", response_model=schemas.GameInDB)
def update_game(game_id: int, game: schemas.GameUpdate, db: Session = Depends(get_db)):
    """
    更新游戏
    
    Args:
        game_id: 游戏ID
        game: 更新的游戏数据
        db: 数据库会话
    
    Returns:
        GameInDB: 更新后的游戏对象
    
    Raises:
        HTTPException: 当游戏不存在时
    """
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # 验证JSON格式（如果提供了相关字段）
    if game.robots is not None:
        validate_json_string(game.robots, "robots")
    if game.walls is not None:
        validate_json_string(game.walls, "walls")
    if game.target is not None:
        validate_json_string(game.target, "target")
    
    update_data = game.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_game, key, value)
    
    db.commit()
    db.refresh(db_game)
    return db_game

@app.delete("/games/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db)):
    """
    删除游戏
    
    Args:
        game_id: 游戏ID
        db: 数据库会话
    
    Returns:
        dict: 删除结果
    
    Raises:
        HTTPException: 当游戏不存在时
    """
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    
    db.delete(db_game)
    db.commit()
    return {"message": "Game deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 