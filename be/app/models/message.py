from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class Message(BaseModel):
    """消息模型"""

    id: str
    thread_id: str
    role: Literal["user", "assistant", "tool"]
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    """创建消息请求模型"""

    content: str = Field(..., min_length=1, max_length=10000)
