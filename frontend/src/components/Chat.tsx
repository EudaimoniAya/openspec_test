import { useState } from 'react'
import { streamChat } from '../api/chat'
import { getSessionId } from '../utils/session'
import './Chat.css'

export type Message = {
  id: string
  role: 'user' | 'assistant'
  content: string
}

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [streaming, setStreaming] = useState(false)

  const sendMessage = async () => {
    const text = input.trim()
    if (!text || streaming) {
      return
    }

    setError(null)
    setInput('')
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
    }
    const assistantId = crypto.randomUUID()
    setMessages((prev) => [...prev, userMessage, { id: assistantId, role: 'assistant', content: '' }])
    setStreaming(true)

    await streamChat(getSessionId(), text, {
      onToken: (token) => {
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantId ? { ...msg, content: msg.content + token } : msg,
          ),
        )
      },
      onError: (message) => {
        setError(message)
      },
      onDone: () => {
        setStreaming(false)
      },
    })
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      void sendMessage()
    }
  }

  return (
    <div className="chat-app">
      <header className="chat-header">
        <h1>AI Chat</h1>
        <p>DeepSeek · 多轮对话</p>
      </header>

      <main className="chat-main" data-testid="chat-main">
        {messages.length === 0 && (
          <p className="chat-empty" data-testid="chat-empty">
            输入问题开始对话
          </p>
        )}
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-bubble chat-bubble--${msg.role}`}>
            {msg.content}
            {streaming && msg.role === 'assistant' && msg.content === '' && (
              <span className="chat-cursor">▌</span>
            )}
          </div>
        ))}
        {error && (
          <p className="chat-error" data-testid="chat-error">
            {error}
          </p>
        )}
      </main>

      <footer className="chat-footer">
        <input
          type="text"
          value={input}
          placeholder="输入你的问题..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={streaming}
          data-testid="chat-input"
        />
        <button type="button" onClick={() => void sendMessage()} disabled={streaming} data-testid="chat-send">
          发送
        </button>
      </footer>
    </div>
  )
}
