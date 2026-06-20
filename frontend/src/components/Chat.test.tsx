import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Chat } from './Chat'

function mockStream(tokens: string[]) {
  const encoder = new TextEncoder()
  const chunks = [
    ...tokens.map((token) => encoder.encode(`data: ${JSON.stringify({ token })}\n\n`)),
    encoder.encode('data: [DONE]\n\n'),
  ]

  let index = 0
  const reader = {
    read: vi.fn(async () => {
      if (index >= chunks.length) {
        return { done: true, value: undefined }
      }
      const value = chunks[index]
      index += 1
      return { done: false, value }
    }),
  }

  vi.stubGlobal(
    'fetch',
    vi.fn(async () => ({
      ok: true,
      body: { getReader: () => reader },
    })),
  )
}

describe('Chat', () => {
  beforeEach(() => {
    vi.unstubAllGlobals()
    sessionStorage.clear()
  })

  it('renders empty state', () => {
    render(<Chat />)
    expect(screen.getByTestId('chat-empty')).toBeInTheDocument()
  })

  it('shows user message after send', async () => {
    mockStream(['回', '复'])
    const user = userEvent.setup()
    render(<Chat />)

    await user.type(screen.getByTestId('chat-input'), '你好')
    await user.click(screen.getByTestId('chat-send'))

    const main = screen.getByTestId('chat-main')
    expect(main.querySelector('.chat-bubble--user')).toHaveTextContent('你好')
  })

  it('does not send blank input', async () => {
    const fetchMock = vi.fn()
    vi.stubGlobal('fetch', fetchMock)

    const user = userEvent.setup()
    render(<Chat />)

    await user.click(screen.getByTestId('chat-send'))
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('appends streamed assistant tokens', async () => {
    mockStream(['你', '好'])
    const user = userEvent.setup()
    render(<Chat />)

    await user.type(screen.getByTestId('chat-input'), 'hello')
    await user.click(screen.getByTestId('chat-send'))

    expect(await screen.findByText('你好')).toBeInTheDocument()
  })

  it('shows error on failed request', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => ({
        ok: false,
        status: 503,
        body: null,
      })),
    )

    const user = userEvent.setup()
    render(<Chat />)

    await user.type(screen.getByTestId('chat-input'), 'hi')
    await user.click(screen.getByTestId('chat-send'))

    expect(await screen.findByTestId('chat-error')).toHaveTextContent('请求失败: 503')
  })
})
