"""LangChain 聊天服务。"""

from collections.abc import AsyncIterator

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL
from app.memory.session_store import SessionStore


class MissingApiKeyError(Exception):
    """未配置 DEEPSEEK_API_KEY。"""


class ChatService:
    """封装 LangChain 流式对话与短期记忆。"""

    def __init__(
        self,
        session_store: SessionStore,
        llm: BaseChatModel | None = None,
        *,
        require_api_key: bool = True,
    ) -> None:
        self._session_store = session_store
        self._llm = llm
        self._require_api_key = require_api_key

    def _resolve_llm(self) -> BaseChatModel:
        if self._llm is not None:
            return self._llm
        if self._require_api_key and not DEEPSEEK_API_KEY:
            raise MissingApiKeyError("DEEPSEEK_API_KEY is not configured")
        return ChatOpenAI(
            model=DEEPSEEK_MODEL,
            api_key=SecretStr(DEEPSEEK_API_KEY or "test-key"),
            base_url=DEEPSEEK_BASE_URL,
            streaming=True,
        )

    async def stream(self, session_id: str, message: str) -> AsyncIterator[str]:
        """流式生成回复，结束后写入 memory。"""
        history = self._session_store.get_history(session_id)
        messages = [*history.messages, HumanMessage(content=message)]

        llm = self._resolve_llm()
        full_response = ""

        async for chunk in llm.astream(messages):
            token = chunk.content
            if isinstance(token, str) and token:
                full_response += token
                yield token

        history.add_user_message(message)
        history.add_ai_message(full_response)

    def get_history_text(self, session_id: str) -> str:
        """获取会话历史文本，供测试断言。"""
        history = self._session_store.get_history(session_id)
        lines: list[str] = []
        for msg in history.messages:
            lines.append(f"{msg.type}: {msg.content}")
        return "\n".join(lines)
