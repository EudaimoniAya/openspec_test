"""聊天 API 路由。"""

import json
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatStreamRequest
from app.services.chat_service import ChatService, MissingApiKeyError

router = APIRouter(prefix="/api", tags=["chat"])


def get_chat_service() -> ChatService:
    """默认 ChatService 依赖（main 模块会覆盖实例）。"""
    from app.main import chat_service

    return chat_service


async def _sse_stream(session_id: str, message: str, service: ChatService) -> AsyncIterator[str]:
    try:
        async for token in service.stream(session_id, message):
            payload = json.dumps({"token": token}, ensure_ascii=False)
            yield f"data: {payload}\n\n"
        yield "data: [DONE]\n\n"
    except MissingApiKeyError as exc:
        payload = json.dumps({"error": str(exc)}, ensure_ascii=False)
        yield f"data: {payload}\n\n"
        yield "data: [DONE]\n\n"


@router.post("/chat/stream")
async def chat_stream(
    body: ChatStreamRequest,
    service: ChatService = Depends(get_chat_service),
) -> StreamingResponse:
    """SSE 流式聊天接口。"""
    try:
        return StreamingResponse(
            _sse_stream(body.session_id, body.message, service),
            media_type="text/event-stream",
        )
    except MissingApiKeyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
