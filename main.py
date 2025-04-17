from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI 服务",
    description="一个基于 FastAPI 的 Web 服务",
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

@app.get("/")
async def root():
    """
    根路由，返回欢迎信息
    
    Returns:
        dict: 包含欢迎信息的字典
    """
    return {"message": "欢迎使用 FastAPI 服务"}

@app.get("/health")
async def health_check():
    """
    健康检查接口
    
    Returns:
        dict: 包含服务状态的字典
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 