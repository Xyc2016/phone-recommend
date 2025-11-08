import json
import logging
from typing import AsyncIterator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.models.message import Message, MessageCreate
from app.services.chat_service import chat_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/threads/{thread_id}/messages", tags=["messages"])


@router.post("")
async def send_message(thread_id: str, message_data: MessageCreate):
    """
    发送消息并获取 AI 响应（SSE 流式响应）
    
    首先添加用户消息，然后流式返回 AI 响应
    """
    logger.info("Received message for thread %s", thread_id)
    # 添加用户消息
    await chat_service.add_message(thread_id, message_data)
    
    # 生成流式响应
    async def generate_sse() -> AsyncIterator[str]:
        """生成 SSE 格式的流式响应"""
        try:
            async for chunk in chat_service.generate_response_stream(thread_id):
                logger.debug("Streaming chunk for thread %s", thread_id)
                # SSE 格式: data: {content}\n\n
                data = json.dumps({"content": chunk}, ensure_ascii=False)
                yield f"data: {data}\n\n"

            # 发送结束标记
            logger.debug("Completed streaming for thread %s", thread_id)
            yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"
        except Exception as e:
            # 发送错误信息
            logger.exception("SSE streaming error for thread %s", thread_id)
            error_data = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate_sse(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("", response_model=list[Message])
async def get_messages(thread_id: str):
    """获取对话消息列表"""
    thread = await chat_service.get_thread(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread.messages

