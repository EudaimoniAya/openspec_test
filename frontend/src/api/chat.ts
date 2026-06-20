export type StreamHandlers = {
  onToken: (token: string) => void
  onError: (message: string) => void
  onDone: () => void
}

/** 调用 SSE 流式聊天 API。 */
export async function streamChat(
  sessionId: string,
  message: string,
  handlers: StreamHandlers,
): Promise<void> {
  const response = await fetch('/api/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message }),
  })

  if (!response.ok) {
    handlers.onError(`请求失败: ${response.status}`)
    handlers.onDone()
    return
  }

  const reader = response.body?.getReader()
  if (!reader) {
    handlers.onError('无法读取响应流')
    handlers.onDone()
    return
  }

  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) {
      break
    }

    buffer += decoder.decode(value, { stream: true })
    const parts = buffer.split('\n\n')
    buffer = parts.pop() ?? ''

    for (const part of parts) {
      const line = part.trim()
      if (!line.startsWith('data:')) {
        continue
      }
      const payload = line.slice(5).trim()
      if (payload === '[DONE]') {
        handlers.onDone()
        return
      }
      try {
        const data = JSON.parse(payload) as { token?: string; error?: string }
        if (data.error) {
          handlers.onError(data.error)
        } else if (data.token) {
          handlers.onToken(data.token)
        }
      } catch {
        handlers.onError('解析 SSE 数据失败')
      }
    }
  }

  handlers.onDone()
}
