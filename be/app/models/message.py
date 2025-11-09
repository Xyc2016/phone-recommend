from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

from app.models.base import MongoModel


class Message(MongoModel):
    """消息模型"""

    thread_id: str
    role: Literal["user", "assistant", "tool", "unknown"]
    content: str
    created_at: datetime
    tool_call_id: str | None = None

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    """创建消息请求模型"""

    content: str = Field(..., min_length=1, max_length=10000)
