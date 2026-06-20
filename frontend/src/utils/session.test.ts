import { describe, expect, it, beforeEach } from 'vitest'
import { getSessionId, resetSessionId } from './session'

describe('getSessionId', () => {
  beforeEach(() => {
    resetSessionId()
  })

  it('creates and reuses session id', () => {
    const first = getSessionId()
    const second = getSessionId()
    expect(first).toBe(second)
    expect(first.length).toBeGreaterThan(0)
  })
})
