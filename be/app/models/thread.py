from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from .message import Message


class Thread(BaseModel):
    """对话线程模型"""

    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []

    class Config:
        from_attributes = True


class ThreadCreate(BaseModel):
    """创建对话线程请求模型"""

    title: Optional[str] = Field(None, max_length=200)


class ThreadUpdate(BaseModel):
    """更新对话线程请求模型"""

    title: Optional[str] = Field(None, max_length=200)
