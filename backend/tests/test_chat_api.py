"""聊天 API 测试。"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.memory.session_store import SessionStore
from app.routers import chat
from app.services.chat_service import ChatService


@pytest.mark.asyncio
async def test_chat_stream_missing_session_id(client: AsyncClient) -> None:
    response = await client.post("/api/chat/stream", json={"message": "hello"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_stream_missing_message(client: AsyncClient) -> None:
    response = await client.post("/api/chat/stream", json={"session_id": "s1"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_stream_empty_session_id(client: AsyncClient) -> None:
    response = await client.post("/api/chat/stream", json={"session_id": "", "message": "hi"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_stream_success(client: AsyncClient) -> None:
    response = await client.post(
        "/api/chat/stream",
        json={"session_id": "session-1", "message": "你好"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")

    body = response.text
    assert 'data: {"token": "你"}' in body
    assert 'data: {"token": "好"}' in body
    assert "data: [DONE]" in body


@pytest.mark.asyncio
async def test_chat_stream_missing_api_key_returns_error_in_sse() -> None:
    store = SessionStore()
    service = ChatService(session_store=store, llm=None, require_api_key=True)
    app.dependency_overrides[chat.get_chat_service] = lambda: service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/chat/stream",
            json={"session_id": "s1", "message": "hi"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "DEEPSEEK_API_KEY" in response.text


@pytest.mark.asyncio
async def test_cors_allows_frontend_origin(client: AsyncClient) -> None:
    response = await client.options(
        "/api/chat/stream",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
