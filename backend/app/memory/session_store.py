"""按 session_id 隔离的 LangChain 短期记忆存储。"""

from langchain_core.chat_history import InMemoryChatMessageHistory


class SessionStore:
    """进程内 session_id → InMemoryChatMessageHistory 映射（LangChain 1.x 等价于 BufferMemory）。"""

    def __init__(self) -> None:
        self._sessions: dict[str, InMemoryChatMessageHistory] = {}

    def get_history(self, session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in self._sessions:
            self._sessions[session_id] = InMemoryChatMessageHistory()
        return self._sessions[session_id]

    def session_count(self) -> int:
        return len(self._sessions)
