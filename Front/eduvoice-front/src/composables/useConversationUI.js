import { computed, ref, watch } from 'vue'
import { useSpeechToText } from './useSpeechToText.js'
import { useVoiceAPI } from './useVoiceAPI.js'
import { useAudioPlayer } from './useAudioPlayer.js'

const SUGGESTIONS = [
  '¿Qué materias debo tomar este semestre?',
  '¿Cómo puedo mejorar mi rendimiento académico?',
  '¿Qué requisitos necesito para graduarme?',
  'Cuéntame sobre las opciones de especialización',
]

function formatTime(date = new Date()) {
  return date.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })
}

function createId() {
  return globalThis.crypto?.randomUUID?.() ?? `msg-${Date.now()}-${Math.random()}`
}

function normalizeQuestion(text) {
  if (!text || typeof text !== 'string') {
    return ''
  }

  return text.trim().replace(/\s+/g, ' ')
}

function cleanQuestion(text) {
  return normalizeQuestion(text).replace(/[^\w\sáéíóúñ¿?!.,]/giu, '').trim()
}

function validateQuestion(text) {
  const normalized = normalizeQuestion(text)

  if (!normalized) {
    return {
      valid: false,
      message: 'Escribe una pregunta antes de enviarla.',
      value: '',
    }
  }

  const cleaned = cleanQuestion(normalized)

  if (!cleaned) {
    return {
      valid: false,
      message: 'La pregunta no contiene texto válido.',
      value: '',
    }
  }

  if (cleaned.length > 500) {
    return {
      valid: false,
      message: 'La pregunta supera el máximo de 500 caracteres.',
      value: cleaned,
    }
  }

  return {
    valid: true,
    message: '',
    value: cleaned,
  }
}

export function useConversationUI(initialUserId = null) {
  const messages = ref([])
  const draft = ref('')
  const status = ref('idle')
  const errorMessage = ref('')

  // Integración con Speech-to-Text
  const { transcript, isListening, error: sttError, startListening, stopListening } = useSpeechToText()

  // Integración con API Backend
  const { processVoice, error: apiError, isProcessing } = useVoiceAPI()

  // Integración con reproductor de audio
  const { playAudio: playAudioFile, isPlaying } = useAudioPlayer()

  // IDs para sesión y usuario
  const sessionId = ref(createId())
  const userId = ref(initialUserId)

  const isEmpty = computed(() => messages.value.length === 0)
  const isRecording = computed(() => isListening.value)
  const isLoading = computed(() => status.value === 'loading' || isProcessing.value)
  const hasError = computed(() => status.value === 'error' && Boolean(errorMessage.value))

  // Cuando termina la grabación, agregar transcript al draft
  watch(isListening, (newVal) => {
    if (!newVal && transcript.value) {
      draft.value = transcript.value
      console.log('Transcript added to draft:', transcript.value)
    }
  })

  // Mostrar errores de STT
  watch(sttError, (newError) => {
    if (newError) {
      errorMessage.value = newError
      status.value = 'error'
      console.error('STT Error:', newError)
    }
  })

  // Mostrar errores de API
  watch(apiError, (newError) => {
    if (newError) {
      errorMessage.value = newError
      status.value = 'error'
      console.error('API Error:', newError)
    }
  })

  function clearError() {
    errorMessage.value = ''
    if (status.value === 'error') status.value = 'idle'
  }

  async function requestAssistantResponse(userText) {
    try {
      status.value = 'loading'
      
      // Llamar al backend
      const result = await processVoice(userText, userId.value, sessionId.value)

      if (!result) {
        throw new Error('No response from API')
      }

      // Agregar respuesta del asistente
      messages.value.push({
        id: createId(),
        role: 'assistant',
        text: result.textResponse,
        audioUrl: result.audioUrl,
        time: formatTime(),
      })

      // Reproducir audio automáticamente
      if (result.audioUrl) {
        console.log('Playing audio from:', result.audioUrl)
        playAudioFile(result.audioUrl)
      }

      status.value = 'success'
    } catch (err) {
      console.error('Error requesting assistant response:', err)
      errorMessage.value = err.message || 'Error al procesar tu solicitud'
      status.value = 'error'
    }
  }

  function submitUserQuery(text) {
    const { valid, message, value: query } = validateQuestion(text)

    if (isLoading.value) return

    if (!valid) {
      errorMessage.value = message
      status.value = 'error'
      return
    }

    clearError()

    // Agregar mensaje del usuario
    messages.value.push({
      id: createId(),
      role: 'user',
      text: query,
      time: formatTime(),
    })

    draft.value = ''
    
    // Solicitar respuesta del asistente
    requestAssistantResponse(query)
  }

  function applySuggestion(text) {
    draft.value = text
    clearError()
  }

  function toggleRecording() {
    clearError()
    if (isLoading.value) return

    if (isListening.value) {
      stopListening()
    } else {
      draft.value = ''
      startListening()
    }
  }

  function sendMessage() {
    if (isListening.value) {
      stopListening()
    }
    submitUserQuery(draft.value)
  }

  function dismissError() {
    clearError()
  }

  return {
    messages,
    draft,
    status,
    errorMessage,
    suggestions: SUGGESTIONS,
    isEmpty,
    isRecording,
    isLoading,
    hasError,
    isPlaying,
    applySuggestion,
    toggleRecording,
    sendMessage,
    dismissError,
  }
}
