"""pytest 公共 fixtures。"""

from collections.abc import AsyncIterator
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field

from app.main import app
from app.memory.session_store import SessionStore
from app.routers import chat
from app.services.chat_service import ChatService


class FakeStreamingLLM(BaseChatModel):
    """测试用流式 LLM，按固定 token 列表输出。"""

    tokens: list[str] = Field(default_factory=lambda: ["你", "好"])
    last_messages: list[BaseMessage] = Field(default_factory=list, exclude=True)

    @property
    def _llm_type(self) -> str:
        return "fake-streaming"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        content = "".join(self.tokens)
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

    async def astream(
        self,
        messages: list[BaseMessage],
        **kwargs: Any,
    ) -> AsyncIterator[AIMessage]:
        self.last_messages = list(messages)
        for token in self.tokens:
            yield AIMessage(content=token)


@pytest.fixture
def session_store() -> SessionStore:
    return SessionStore()


@pytest.fixture
def fake_llm() -> FakeStreamingLLM:
    return FakeStreamingLLM()


@pytest.fixture
def chat_service(session_store: SessionStore, fake_llm: FakeStreamingLLM) -> ChatService:
    return ChatService(session_store=session_store, llm=fake_llm, require_api_key=False)


@pytest.fixture
async def client(chat_service: ChatService) -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[chat.get_chat_service] = lambda: chat_service
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
