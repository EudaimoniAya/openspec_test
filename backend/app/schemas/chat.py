"""聊天相关 Pydantic 模型。"""

from pydantic import BaseModel, Field


class ChatStreamRequest(BaseModel):
    """流式聊天请求体。"""

    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
