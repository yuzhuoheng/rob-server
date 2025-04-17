# FastAPI 服务

这是一个基于 FastAPI 的 Web 服务框架。

## 功能特性

- 基于 FastAPI 框架
- 支持 CORS
- 自动 API 文档生成
- 健康检查接口

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python main.py
```

服务将在 http://localhost:8000 启动

## API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要接口

- GET / : 根路由，返回欢迎信息
- GET /health : 健康检查接口 
