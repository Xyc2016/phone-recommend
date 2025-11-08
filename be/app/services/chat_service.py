import logging
from typing import AsyncIterator, List, Optional

from bson import ObjectId
from fastapi import HTTPException
from langchain.messages import AIMessage, ToolMessage
from pymongo import ReturnDocument

from app.database import get_threads_collection
from app.models.message import Message, MessageCreate
from app.models.thread import Thread, ThreadCreate, ThreadUpdate
from app.services.llm_service import llm_service
from app.utils.datetime import now

logger = logging.getLogger("app.chat_service")


class ChatService:
    """对话服务"""

    @staticmethod
    async def create_thread(thread_data: ThreadCreate) -> Thread:
        """创建对话线程"""
        threads_collection = get_threads_collection()

        thread_doc = {
            "title": thread_data.title or "新对话",
            "created_at": now(),
            "updated_at": now(),
            "messages": [],
        }

        result = await threads_collection.insert_one(thread_doc)
        logger.info("Created thread %s", result.inserted_id)
        thread_doc["id"] = str(result.inserted_id)
        thread_doc["_id"] = result.inserted_id

        return Thread(
            id=str(result.inserted_id),
            title=thread_doc["title"],
            created_at=thread_doc["created_at"],
            updated_at=thread_doc["updated_at"],
            messages=[],
        )

    @staticmethod
    async def get_thread(thread_id: str) -> Optional[Thread]:
        """获取对话线程"""
        threads_collection = get_threads_collection()

        thread_doc = await threads_collection.find_one({"_id": ObjectId(thread_id)})
        if not thread_doc:
            logger.warning("Thread %s not found", thread_id)
            return None

        messages = [
            Message(
                id=str(msg.get("_id", "")),
                thread_id=thread_id,
                role=msg["role"],
                content=msg["content"],
                created_at=msg["created_at"],
            )
            for msg in thread_doc.get("messages", [])
        ]

        return Thread(
            id=str(thread_doc["_id"]),
            title=thread_doc["title"],
            created_at=thread_doc["created_at"],
            updated_at=thread_doc["updated_at"],
            messages=messages,
        )

    @staticmethod
    async def list_threads(limit: int = 100, skip: int = 0) -> List[Thread]:
        """获取对话线程列表"""
        threads_collection = get_threads_collection()

        cursor = threads_collection.find().sort("updated_at", -1).skip(skip).limit(limit)
        threads: List[Thread] = []

        async for thread_doc in cursor:
            threads.append(
                Thread(
                    id=str(thread_doc["_id"]),
                    title=thread_doc["title"],
                    created_at=thread_doc["created_at"],
                    updated_at=thread_doc["updated_at"],
                    messages=[],  # 列表时不返回完整消息
                )
            )

        logger.debug("Fetched %d threads", len(threads))
        return threads

    @staticmethod
    async def update_thread(thread_id: str, update_data: ThreadUpdate) -> Thread:
        """更新对话线程"""
        threads_collection = get_threads_collection()

        update_payload = {}

        if update_data.title is not None:
            new_title = update_data.title.strip()
            if not new_title:
                logger.warning("Attempted to update thread %s with empty title", thread_id)
                raise HTTPException(status_code=400, detail="Title cannot be empty")
            update_payload["title"] = new_title

        if not update_payload:
            logger.warning("No update fields provided for thread %s", thread_id)
            raise HTTPException(status_code=400, detail="No update fields provided")

        update_payload["updated_at"] = now()

        updated_thread = await threads_collection.find_one_and_update(
            {"_id": ObjectId(thread_id)},
            {"$set": update_payload},
            return_document=ReturnDocument.AFTER,
        )

        if not updated_thread:
            logger.warning("Thread %s not found when updating", thread_id)
            raise HTTPException(status_code=404, detail="Thread not found")

        messages = [
            Message(
                id=str(msg.get("_id", "")),
                thread_id=thread_id,
                role=msg["role"],
                content=msg["content"],
                created_at=msg["created_at"],
            )
            for msg in updated_thread.get("messages", [])
        ]

        logger.info("Updated thread %s", thread_id)

        return Thread(
            id=str(updated_thread["_id"]),
            title=updated_thread["title"],
            created_at=updated_thread["created_at"],
            updated_at=updated_thread["updated_at"],
            messages=messages,
        )

    @staticmethod
    async def delete_thread(thread_id: str) -> bool:
        """删除对话线程"""
        threads_collection = get_threads_collection()

        result = await threads_collection.delete_one({"_id": ObjectId(thread_id)})
        if result.deleted_count:
            logger.info("Deleted thread %s", thread_id)
        else:
            logger.warning("Attempted to delete missing thread %s", thread_id)
        return result.deleted_count > 0

    @staticmethod
    async def add_message(thread_id: str, message_data: MessageCreate) -> Message:
        """添加用户消息"""
        threads_collection = get_threads_collection()

        # 检查线程是否存在
        thread = await threads_collection.find_one({"_id": ObjectId(thread_id)})
        if not thread:
            logger.warning("Thread %s not found when adding message", thread_id)
            raise HTTPException(status_code=404, detail="Thread not found")

        # 创建用户消息
        user_message = {
            "_id": ObjectId(),
            "role": "user",
            "content": message_data.content,
            "created_at": now(),
        }

        # 更新线程
        await threads_collection.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$push": {"messages": user_message},
                "$set": {"updated_at": now()},
            },
        )
        logger.debug("Added user message to thread %s", thread_id)

        # 如果是第一条消息，更新标题
        if len(thread.get("messages", [])) == 0:
            title = message_data.content[:50] + "..." if len(message_data.content) > 50 else message_data.content
            await threads_collection.update_one(
                {"_id": ObjectId(thread_id)},
                {"$set": {"title": title}},
            )
            logger.debug("Updated title for thread %s", thread_id)

        return Message(
            id=str(user_message["_id"]),
            thread_id=thread_id,
            role="user",
            content=user_message["content"],
            created_at=user_message["created_at"],
        )

    @staticmethod
    async def generate_response_stream(thread_id: str) -> AsyncIterator[str]:
        """
        生成 AI 响应（流式）

        Args:
            thread_id: 对话线程 ID

        Yields:
            str: 响应文本片段
        """
        threads_collection = get_threads_collection()

        # 获取线程和消息历史
        thread = await threads_collection.find_one({"_id": ObjectId(thread_id)})
        if not thread:
            logger.warning("Thread %s not found when generating response", thread_id)
            raise HTTPException(status_code=404, detail="Thread not found")

        # 格式化消息历史
        messages_history = [{"role": msg["role"], "content": msg["content"]} for msg in thread.get("messages", [])]

        # 转换为 LangChain 消息格式
        langchain_messages = llm_service.format_messages(messages_history)

        # 流式生成响应
        logger.debug("Start streaming response for thread %s", thread_id)
        message_sub_docs = []
        async for message in llm_service.agent_stream(langchain_messages):
            yield str(message.content)
            role = None
            if isinstance(message, AIMessage):
                role = "assistant"
            elif isinstance(message, ToolMessage):
                role = "tool"
            else:
                role = "unknown"
                logger.error("Unknown message role: %s", message)
            message_sub_docs.append(
                {
                    "_id": ObjectId(),
                    "role": role,
                    "content": message.content,
                    "created_at": now(),
                }
            )

            # 保存 AI 响应到数据库

        await threads_collection.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$push": {"messages": {"$each": message_sub_docs}},
                "$set": {"updated_at": now()},
            },
        )
        logger.debug("Saved assistant response for thread %s", thread_id)


chat_service = ChatService()
