import logging
from typing import Optional

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

from app.config import settings

logger = logging.getLogger("app.database")


class Database:
    client: Optional[AsyncIOMotorClient] = None
    threads_collection: Optional[AsyncIOMotorCollection] = None
    phones_collection: Optional[AsyncIOMotorCollection] = None


db = Database()


async def connect_to_mongo() -> None:
    """连接 MongoDB"""
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    database = db.client[settings.mongodb_db_name]
    db.threads_collection = database.get_collection("threads")
    db.phones_collection = database.get_collection("phones")
    logger.info("Connected to MongoDB database '%s'", settings.mongodb_db_name)


async def close_mongo_connection() -> None:
    """关闭 MongoDB 连接"""
    if db.client:
        db.client.close()
        db.client = None
        db.threads_collection = None
        db.phones_collection = None
        logger.info("Disconnected from MongoDB")


def get_database() -> AsyncIOMotorDatabase:
    """获取数据库实例"""
    if not db.client:
        raise RuntimeError("MongoDB client is not initialized")
    return db.client[settings.mongodb_db_name]


def get_threads_collection() -> AsyncIOMotorCollection:
    """获取对话线程集合"""
    if db.threads_collection is None:
        if not db.client:
            raise RuntimeError("MongoDB client is not initialized")
        database = db.client[settings.mongodb_db_name]
        db.threads_collection = database.get_collection("threads")
    return db.threads_collection


def get_phones_collection() -> AsyncIOMotorCollection:
    """获取手机数据集合"""
    if db.phones_collection is None:
        if not db.client:
            raise RuntimeError("MongoDB client is not initialized")
        database = db.client[settings.mongodb_db_name]
        db.phones_collection = database.get_collection("phones")
    return db.phones_collection
