import logging
from typing import AsyncIterator, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from app.config import settings

logger = logging.getLogger("app.llm")


class LLMService:
    """LLM 服务"""

    def __init__(self) -> None:
        client_kwargs: Dict[str, Any] = {
            "model": settings.openai_model,
            "temperature": 0.7,
            "streaming": True,
            "api_key": settings.openai_api_key,
        }
        if settings.openai_api_base:
            client_kwargs["base_url"] = settings.openai_api_base

        self.llm = ChatOpenAI(**client_kwargs)
        logger.info("Initialized ChatOpenAI model %s", settings.openai_model)

    async def chat_stream(
        self,
        messages: list[BaseMessage]
    ) -> AsyncIterator[str]:
        """
        流式聊天

        Args:
            messages: 消息列表

        Yields:
            str: 流式返回的文本片段
        """
        async for chunk in self.llm.astream(messages):
            content = chunk.content
            if not content:
                continue
            if not isinstance(content, str):
                content = "".join(
                    part.text if hasattr(part, "text") else str(part)
                    for part in content  # type: ignore[arg-type]
                )
            logger.debug("LLM chunk: %s", content)
            if content:
                yield content

    def format_messages(self, history: list[dict]) -> list[BaseMessage]:
        """
        格式化消息历史为 LangChain 消息格式
        
        Args:
            history: 消息历史列表，每个元素包含 role 和 content
            
        Returns:
            list[BaseMessage]: LangChain 消息列表
        """
        formatted = []
        for msg in history:
            if msg["role"] == "user":
                formatted.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                formatted.append(AIMessage(content=msg["content"]))
        return formatted


llm_service = LLMService()

