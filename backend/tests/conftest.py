"""pytest 公共 fixtures。"""

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from langchain_core.messages import AIMessage

from app.main import app
from app.memory.session_store import SessionStore
from app.routers import chat
from app.services.chat_service import ChatService


class FakeStreamingLLM:
    """测试用流式 LLM，按固定 token 列表输出。"""

    def __init__(self, tokens: list[str] | None = None) -> None:
        self._tokens = tokens or ["你", "好"]
        self.last_messages: list = []

    async def astream(self, messages: list) -> AsyncIterator[AIMessage]:
        self.last_messages = messages
        for token in self._tokens:
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
