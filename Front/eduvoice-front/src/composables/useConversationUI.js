import { computed, ref, watch } from 'vue'
import { useSpeechToText } from './useSpeechToText.js'

const SUGGESTIONS = [
  '¿Qué materias debo tomar este semestre?',
  '¿Cómo puedo mejorar mi rendimiento académico?',
  '¿Qué requisitos necesito para graduarme?',
  'Cuéntame sobre las opciones de especialización',
]

const DEMO_RESPONSE_MS = 1400

function formatTime(date = new Date()) {
  return date.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })
}

function createId() {
  return globalThis.crypto?.randomUUID?.() ?? `msg-${Date.now()}-${Math.random()}`
}

export function useConversationUI() {
  const messages = ref([])
  const draft = ref('')
  const status = ref('idle')
  const errorMessage = ref('')

  // Integración con Speech-to-Text
  const { transcript, isListening, error: sttError, startListening, stopListening } = useSpeechToText()

  const isEmpty = computed(() => messages.value.length === 0)
  const isRecording = computed(() => isListening.value)
  const isLoading = computed(() => status.value === 'loading')
  const hasError = computed(() => status.value === 'error' && Boolean(errorMessage.value))

  // Cuando termina la grabación, agregar transcript al draft
  watch(isListening, (newVal) => {
    if (!newVal && transcript.value) {
      // Se terminó la grabación
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

  function clearError() {
    errorMessage.value = ''
    if (status.value === 'error') status.value = 'idle'
  }

  function requestAssistantResponse() {
    window.setTimeout(() => {
      messages.value.push({
        id: createId(),
        role: 'assistant',
        text:
          '¡Hola! Esta es una **respuesta de demostración** en la interfaz.\n\n' +
          'Cuando el backend esté conectado, aquí verás la orientación académica generada por IA.',
        audioUrl: null,
        time: formatTime(),
      })
      status.value = 'success'
    }, DEMO_RESPONSE_MS)
  }

  function submitUserQuery(text) {
    const query = text.trim()
    if (!query || isLoading.value) return

    clearError()
    messages.value.push({
      id: createId(),
      role: 'user',
      text: query,
      time: formatTime(),
    })

    draft.value = ''
    status.value = 'loading'
    requestAssistantResponse()
  }

  function applySuggestion(text) {
    draft.value = text
    clearError()
  }

  function toggleRecording() {
    clearError()
    if (isLoading.value) return

    if (isListening.value) {
      // Detener grabación
      stopListening()
      // El watch se encargará de actualizar el draft
    } else {
      // Iniciar grabación
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
    applySuggestion,
    toggleRecording,
    sendMessage,
    dismissError,
  }
}
