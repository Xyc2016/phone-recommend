import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.api import threads, messages
from app.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("app.main")

app = FastAPI(
    title="手机推荐 AI Agent API",
    description="基于 LangChain 和 OpenAI 的手机推荐助手后端 API",
    version="1.0.0",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(threads.router)
app.include_router(messages.router)


@app.on_event("startup")
async def startup_event():
    """应用启动时连接数据库"""
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时断开数据库连接"""
    await close_mongo_connection()


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "手机推荐 AI Agent API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}

