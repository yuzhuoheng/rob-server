from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Game(Base):
    """
    游戏表模型
    
    Attributes:
        id: 主键ID
        robots: 机器人初始位置和状态（JSON格式的字符串）
        walls: 墙信息（JSON格式的字符串）
        target: 目的地信息（JSON格式的字符串）
        limit: 限时（秒，默认180秒）
    """
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True)
    robots = Column(String(2000), nullable=False)  # JSON格式的机器人信息
    walls = Column(String(2000), nullable=False)   # JSON格式的墙信息
    target = Column(String(2000), nullable=False)  # JSON格式的目标信息
    limit = Column(Integer, default=180)           # 限时，默认180秒 