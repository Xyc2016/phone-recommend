import logging
from typing import Any, AsyncIterator, Dict, List

from langchain.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolCall,
    ToolMessage,
)
from langchain_core.language_models import BaseChatModel, LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.func import task
from langgraph.graph import add_messages
from langgraph.graph.state import Runnable
from rich import print

from app.config import settings
from app.tools import search_phones

logger = logging.getLogger("app.llm")

tools = [search_phones]
tools_by_name = {tool.name: tool for tool in tools}


async def call_tool(tool_call: ToolCall) -> ToolMessage:
    """Performs the tool call and wraps the result in a ToolMessage."""
    tool = tools_by_name[tool_call["name"]]
    print("calling tool", tool_call)
    result = await tool.ainvoke(tool_call)

    if isinstance(result, str):
        content = result
    else:
        content = str(result)

    return ToolMessage(content=content, tool_call_id=tool_call["id"])


@task
async def call_llm(model: ChatOpenAI, messages: list[BaseMessage]) -> AIMessage:
    """LLM decides whether to call a tool or not"""
    return await model.ainvoke(
        [
            SystemMessage(
                content="你是一个手机推荐助手，根据用户的需求，使用search_phones tool从数据库中搜索手机信息，并返回给用户。注意只能推荐数据库里的手机，不能推荐其他手机。"
            )
        ]
        + messages
    )


async def agent_stream_core(
    model: Runnable[LanguageModelInput, AIMessage], messages: list[BaseMessage]
) -> AsyncIterator[BaseMessage]:
    new_messages: list[BaseMessage] = []
    while True:
        input_messages = add_messages(
            [
                SystemMessage(
                    content="你是一个手机推荐助手，根据用户的需求，使用search_phones tool从数据库中搜索手机信息，并返回给用户。注意只能推荐数据库里的手机，不能推荐其他手机。"
                )
            ],
            messages + new_messages,
        )
        model_response = await model.ainvoke(input_messages)
        yield model_response
        if not model_response.tool_calls:
            break

        # Execute tools
        tool_results = [await call_tool(tool_call) for tool_call in model_response.tool_calls]
        for tool_result in tool_results:
            yield tool_result
        new_messages = add_messages(new_messages, [model_response, *tool_results])


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
        self.tools: List[BaseTool] = []
        self.llm_with_tools = self.llm
        logger.info("Initialized ChatOpenAI model %s", settings.openai_model)

    def bind_tools(self, tools: List[BaseTool]) -> None:
        """
        绑定工具到 LLM

        Args:
            tools: 工具列表
        """
        self.tools = tools
        self.llm_with_tools = self.llm.bind_tools(tools)
        logger.info("Bound %d tools to LLM: %s", len(tools), [t.name for t in tools])

    async def chat_stream(
        self,
        messages: list[BaseMessage],
        use_tools: bool = True,
    ) -> AsyncIterator[str]:
        """
        流式聊天，支持工具调用

        Args:
            messages: 消息列表
            use_tools: 是否使用工具

        Yields:
            str: 流式返回的文本片段
        """
        llm = self.llm_with_tools

        # 首次调用 LLM - 累积所有 chunks
        full_response = None
        response_content = ""

        async for chunk in llm.astream(messages):
            if full_response is None:
                full_response = chunk
            else:
                full_response = full_response + chunk

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
                response_content += content
                yield content
        # 检查是否有工具调用
        if full_response and hasattr(full_response, "tool_calls") and full_response.tool_calls:
            logger.info("LLM requested tool calls: %s", full_response.tool_calls)

            # 添加 AI 消息到历史
            messages.append(full_response)

            # 执行工具调用
            for tool_call in full_response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                logger.info("Executing tool: %s with args: %s", tool_name, tool_args)

                # 查找对应的工具
                tool = next((t for t in self.tools if t.name == tool_name), None)

                if tool:
                    try:
                        # 执行工具
                        if hasattr(tool, "coroutine") and tool.coroutine:
                            tool_result = await tool.coroutine(**tool_args)
                        else:
                            tool_result = await tool.ainvoke(tool_args)

                        logger.info("Tool %s result: %s", tool_name, tool_result)

                        # 添加工具结果到消息历史
                        messages.append(
                            ToolMessage(
                                content=str(tool_result),
                                tool_call_id=tool_id,
                            )
                        )
                    except Exception as e:
                        logger.error("Error executing tool %s: %s", tool_name, e, exc_info=True)
                        messages.append(
                            ToolMessage(
                                content=f"工具执行出错：{str(e)}",
                                tool_call_id=tool_id,
                            )
                        )
                else:
                    logger.warning("Tool %s not found", tool_name)
                    messages.append(
                        ToolMessage(
                            content=f"未找到工具：{tool_name}",
                            tool_call_id=tool_id,
                        )
                    )

            # 用工具结果再次调用 LLM
            yield "\n\n"  # 添加换行以分隔工具调用结果

            async for chunk in llm.astream(messages):
                content = chunk.content

                if not content:
                    continue

                if not isinstance(content, str):
                    content = "".join(
                        part.text if hasattr(part, "text") else str(part)
                        for part in content  # type: ignore[arg-type]
                    )

                logger.debug("LLM chunk (after tool): %s", content)

                if content:
                    yield content

    async def agent_stream(self, messages: list[BaseMessage]) -> AsyncIterator[BaseMessage]:
        async for message in agent_stream_core(self.llm_with_tools, messages):
            yield message

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
            elif msg["role"] == "tool":
                formatted.append(ToolMessage(content=msg["content"], tool_call_id=msg["tool_call_id"]))
        return formatted


llm_service = LLMService()
