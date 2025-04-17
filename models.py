from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# 创建数据库引擎
engine = create_engine(settings.DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

class Game(Base):
    """
    游戏表模型
    
    Attributes:
        id: 主键ID
        robots: 机器人初始位置和状态（JSON格式的字符串）
        walls: 墙信息（JSON格式的字符串）
        target: 目的地信息（JSON格式的字符串）
        limit: 限时（秒，默认180秒）
        created_at: 创建时间
    """
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True)
    robots = Column(String(2000), nullable=False)  # JSON格式的机器人信息
    walls = Column(String(2000), nullable=False)   # JSON格式的墙信息
    target = Column(String(2000), nullable=False)  # JSON格式的目标信息
    limit = Column(Integer, default=180)           # 限时，默认180秒
    created_at = Column(DateTime)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 数据库依赖
def get_db():
    """
    获取数据库会话
    
    Yields:
        Session: 数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 