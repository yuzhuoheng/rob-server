from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    应用配置类
    
    Attributes:
        DATABASE_URL: 数据库连接URL
    """
    DATABASE_URL: str = "mysql+pymysql://root:jx665389=@10.33.104.157:3306/robot"

settings = Settings() 