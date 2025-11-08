from fastapi import APIRouter, HTTPException
from app.models.thread import Thread, ThreadCreate, ThreadUpdate
from app.services.chat_service import chat_service
from typing import List

router = APIRouter(prefix="/api/threads", tags=["threads"])


@router.get("", response_model=List[Thread])
async def list_threads(skip: int = 0, limit: int = 100):
    """获取所有对话线程"""
    return await chat_service.list_threads(limit=limit, skip=skip)


@router.post("", response_model=Thread, status_code=201)
async def create_thread(thread_data: ThreadCreate):
    """创建新对话线程"""
    return await chat_service.create_thread(thread_data)


@router.patch("/{thread_id}", response_model=Thread)
async def update_thread(thread_id: str, thread_data: ThreadUpdate):
    """更新对话线程"""
    return await chat_service.update_thread(thread_id, thread_data)


@router.get("/{thread_id}", response_model=Thread)
async def get_thread(thread_id: str):
    """获取单个对话线程"""
    thread = await chat_service.get_thread(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread


@router.delete("/{thread_id}", status_code=204)
async def delete_thread(thread_id: str):
    """删除对话线程"""
    success = await chat_service.delete_thread(thread_id)
    if not success:
        raise HTTPException(status_code=404, detail="Thread not found")
    return None
