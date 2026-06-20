"""ChatService 单元测试。"""

import pytest

from app.memory.session_store import SessionStore
from app.services.chat_service import ChatService
from tests.conftest import FakeStreamingLLM


@pytest.mark.asyncio
async def test_same_session_keeps_history() -> None:
    store = SessionStore()
    llm = FakeStreamingLLM(tokens=["小明"])
    service = ChatService(session_store=store, llm=llm, require_api_key=False)

    tokens = []
    async for token in service.stream("s1", "我叫小明"):
        tokens.append(token)
    assert tokens == ["小明"]

    llm2 = FakeStreamingLLM(tokens=["记得"])
    service2 = ChatService(session_store=store, llm=llm2, require_api_key=False)
    async for _ in service2.stream("s1", "我叫什么"):
        pass

    assert llm2.last_messages
    history_text = service2.get_history_text("s1")
    assert "小明" in history_text


@pytest.mark.asyncio
async def test_different_sessions_are_isolated() -> None:
    store = SessionStore()
    llm_a = FakeStreamingLLM(tokens=["A"])
    service = ChatService(session_store=store, llm=llm_a, require_api_key=False)

    async for _ in service.stream("session-a", "msg-a"):
        pass

    llm_b = FakeStreamingLLM(tokens=["B"])
    service_b = ChatService(session_store=store, llm=llm_b, require_api_key=False)
    async for _ in service_b.stream("session-b", "msg-b"):
        pass

    history_a = service_b.get_history_text("session-a")
    history_b = service_b.get_history_text("session-b")

    assert "msg-a" in history_a
    assert "msg-b" in history_b
    assert "msg-b" not in history_a
    assert "msg-a" not in history_b
