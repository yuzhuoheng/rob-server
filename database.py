from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import time
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库连接URL
DATABASE_URL = "mysql+pymysql://root:jx665389=@10.33.104.157:3306/robot"

# 创建数据库引擎，添加连接池配置
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 允许的最大溢出连接数
    pool_timeout=30,  # 等待连接的超时时间
    pool_recycle=1800,  # 回收连接的时间（秒）
    pool_pre_ping=True,  # 连接前进行ping测试
    connect_args={
        "connect_timeout": 10,  # 连接超时时间
    }
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 定义应该重试的异常类型
def should_retry_exception(exception):
    """判断是否应该重试特定异常"""
    retry_exceptions = (
        exc.OperationalError,  # 数据库操作错误
        exc.DisconnectionError,  # 连接断开错误
        exc.TimeoutError,  # 超时错误
    )
    return isinstance(exception, retry_exceptions)

# 带有重试机制的数据库会话获取函数
@retry(
    retry=retry_if_exception_type(should_retry_exception),
    stop=stop_after_attempt(3),  # 最多重试3次
    wait=wait_fixed(2),  # 每次重试间隔2秒
    before_sleep=lambda retry_state: logger.warning(
        f"数据库连接失败，将在2秒后第{retry_state.attempt_number}次重试。错误: {retry_state.outcome.exception()}"
    )
)
def get_db_with_retry():
    """获取数据库会话，带有重试机制"""
    try:
        db = SessionLocal()
        # 尝试执行一个简单查询以测试连接
        db.execute("SELECT 1")
        return db
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        if hasattr(db, 'close'):
            db.close()
        raise

# 数据库依赖
def get_db():
    """
    获取数据库会话，带有重试机制
    
    Yields:
        Session: 数据库会话
    """
    db = None
    try:
        db = get_db_with_retry()
        yield db
    except Exception as e:
        logger.error(f"数据库操作失败: {str(e)}")
        if db:
            db.rollback()
        raise
    finally:
        if db:
            db.close() 