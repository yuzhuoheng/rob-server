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
        created_at: 创建时间
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 