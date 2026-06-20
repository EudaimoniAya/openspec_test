const SESSION_KEY = 'chat_session_id'

/** 获取或创建浏览器标签页级 session_id。 */
export function getSessionId(): string {
  const existing = sessionStorage.getItem(SESSION_KEY)
  if (existing) {
    return existing
  }
  const id = crypto.randomUUID()
  sessionStorage.setItem(SESSION_KEY, id)
  return id
}

/** 测试用：重置 sessionStorage。 */
export function resetSessionId(): void {
  sessionStorage.removeItem(SESSION_KEY)
}
