"""FastAPI 应用入口。"""

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.memory.session_store import SessionStore
from app.routers import chat
from app.services.chat_service import ChatService

load_dotenv()

app = FastAPI(title="AI Chatbot", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_store = SessionStore()
chat_service = ChatService(session_store=session_store)

app.include_router(chat.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    """健康检查。"""
    return {"status": "ok"}
