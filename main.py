from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import games, users
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由器
app.include_router(games.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    """
    根路径的健康检查端点
    
    Returns:
        dict: 包含欢迎消息的字典
    """
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 