import { beforeEach, describe, expect, it, vi } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import { ref } from 'vue'
import { useConversationUI } from './useConversationUI.js'

const processVoiceMock = vi.fn()
const playAudioMock = vi.fn()

vi.mock('./useSpeechToText.js', () => ({
  useSpeechToText: () => ({
    transcript: ref(''),
    isListening: ref(false),
    error: ref(''),
    startListening: vi.fn(),
    stopListening: vi.fn(),
  }),
}))

vi.mock('./useVoiceAPI.js', () => ({
  useVoiceAPI: () => ({
    processVoice: (...args) => processVoiceMock(...args),
    error: ref(null),
    isProcessing: ref(false),
  }),
}))

vi.mock('./useAudioPlayer.js', () => ({
  useAudioPlayer: () => ({
    playAudio: (...args) => playAudioMock(...args),
    isPlaying: ref(false),
  }),
}))

describe('useConversationUI', () => {
  beforeEach(() => {
    processVoiceMock.mockReset()
    playAudioMock.mockReset()
    processVoiceMock.mockResolvedValue(null)
  })

  it('rejects empty questions', () => {
    const { sendMessage, messages, hasError, errorMessage } = useConversationUI('user-1')

    sendMessage()

    expect(messages.value).toHaveLength(0)
    expect(hasError.value).toBe(true)
    expect(errorMessage.value).toContain('pregunta')
    expect(processVoiceMock).not.toHaveBeenCalled()
  })

  it('sends valid question and adds assistant response', async () => {
    processVoiceMock.mockResolvedValue({
      textResponse: 'Debes cumplir los créditos requeridos.',
      audioUrl: 'data:audio/mp3;base64,xyz',
    })

    const { draft, sendMessage, messages } = useConversationUI('user-42')
    draft.value = '¿Qué requisitos necesito para graduarme?'

    sendMessage()

    expect(messages.value).toHaveLength(1)
    expect(messages.value[0].role).toBe('user')
    expect(draft.value).toBe('')

    await vi.waitFor(() => {
      expect(messages.value).toHaveLength(2)
    })

    expect(messages.value[1].role).toBe('assistant')
    expect(messages.value[1].text).toBe('Debes cumplir los créditos requeridos.')
    expect(playAudioMock).toHaveBeenCalledWith('data:audio/mp3;base64,xyz')
    expect(processVoiceMock).toHaveBeenCalledWith(
      '¿Qué requisitos necesito para graduarme?',
      'user-42',
      expect.any(String),
    )

    await flushPromises()
  })

  it('rejects questions longer than 500 characters', async () => {
    const { draft, sendMessage, hasError } = useConversationUI()
    draft.value = 'a'.repeat(501)

    sendMessage()
    await flushPromises()

    expect(hasError.value).toBe(true)
    expect(processVoiceMock).not.toHaveBeenCalled()
  })

  it('applySuggestion fills the draft', () => {
    const { draft, applySuggestion } = useConversationUI()
    applySuggestion('¿Qué materias debo tomar este semestre?')

    expect(draft.value).toBe('¿Qué materias debo tomar este semestre?')
  })
})
