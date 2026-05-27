import { describe, expect, it, vi } from 'vitest'
import { useVoiceAPI } from './useVoiceAPI.js'

describe('useVoiceAPI', () => {
  it('rejects empty text without calling the API', async () => {
    const fetchMock = vi.fn()
    vi.stubGlobal('fetch', fetchMock)

    const { processVoice, error } = useVoiceAPI()
    const result = await processVoice('   ')

    expect(result).toBeNull()
    expect(error.value).toBe('El texto no puede estar vacío')
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('returns parsed response on success', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: () =>
          Promise.resolve({
            text_response: 'Respuesta del asistente',
            audio_url: 'data:audio/mp3;base64,abc',
            latency_ms: 120,
            status: 'success',
          }),
      }),
    )

    const { processVoice, isProcessing } = useVoiceAPI()
    const result = await processVoice('¿Cómo me gradúo?', 'user-1', 'session-1')

    expect(result).toEqual({
      textResponse: 'Respuesta del asistente',
      audioUrl: 'data:audio/mp3;base64,abc',
      latencyMs: 120,
      status: 'success',
    })
    expect(isProcessing.value).toBe(false)
  })

  it('sets error when API responds with failure', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        json: () => Promise.resolve({ detail: 'LLM processing failed' }),
      }),
    )

    const { processVoice, error } = useVoiceAPI()
    const result = await processVoice('¿Cuáles son los requisitos?')

    expect(result).toBeNull()
    expect(error.value).toBe('LLM processing failed')
  })

  it('checkHealth returns service status', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: () =>
          Promise.resolve({
            status: 'healthy',
            services: { llm: 'ok', tts: 'ok' },
          }),
      }),
    )

    const { checkHealth } = useVoiceAPI()
    const health = await checkHealth()

    expect(health.status).toBe('healthy')
  })
})
