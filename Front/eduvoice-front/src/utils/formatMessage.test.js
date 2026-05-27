import { describe, expect, it } from 'vitest'
import { formatMessage } from './formatMessage.js'

describe('formatMessage', () => {
  it('returns empty string for falsy input', () => {
    expect(formatMessage('')).toBe('')
    expect(formatMessage(null)).toBe('')
    expect(formatMessage(undefined)).toBe('')
  })

  it('escapes HTML characters', () => {
    expect(formatMessage('<script>alert(1)</script>')).toBe(
      '&lt;script&gt;alert(1)&lt;/script&gt;',
    )
  })

  it('converts markdown bold to strong tags', () => {
    expect(formatMessage('Hola **mundo**')).toBe('Hola <strong>mundo</strong>')
  })

  it('converts newlines to br tags', () => {
    expect(formatMessage('línea 1\nlínea 2')).toBe('línea 1<br />línea 2')
  })
})
