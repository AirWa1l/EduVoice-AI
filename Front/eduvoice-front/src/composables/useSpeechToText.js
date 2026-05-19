import { ref, computed } from 'vue'

export function useSpeechToText() {
  const transcript = ref('')
  const isListening = ref(false)
  const error = ref('')
  const isSupported = ref(false)

  // Detectar soporte del navegador
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition

  if (SpeechRecognition) {
    isSupported.value = true
  }

  let recognition = null

  function initializeRecognition() {
    if (!SpeechRecognition) {
      error.value = 'Tu navegador no soporta Speech Recognition'
      console.error('Speech Recognition API not supported')
      return
    }

    recognition = new SpeechRecognition()

    // Configurar idioma a español
    recognition.lang = 'es-CO'
    recognition.continuous = false
    recognition.interimResults = true
    recognition.maxAlternatives = 1

    // Evento: se inicia la escucha
    recognition.onstart = () => {
      console.log('Speech recognition started')
      isListening.value = true
      error.value = ''
      transcript.value = ''
    }

    // Evento: se reciben resultados
    recognition.onresult = (event) => {
      let interimTranscript = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcriptSegment = event.results[i][0].transcript

        if (event.results[i].isFinal) {
          transcript.value += transcriptSegment + ' '
        } else {
          interimTranscript += transcriptSegment
        }
      }

      // Mostrar transcripción en tiempo real
      if (interimTranscript) {
        console.log('Interim:', interimTranscript)
      }
    }

    // Evento: error
    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error)
      error.value = getErrorMessage(event.error)
    }

    // Evento: se termina
    recognition.onend = () => {
      console.log('Speech recognition ended')
      isListening.value = false
      // Limpiar espacios extras
      transcript.value = transcript.value.trim()
    }
  }

  function getErrorMessage(errorCode) {
    const errors = {
      'no-speech': 'No se detectó voz. Intenta de nuevo.',
      'audio-capture': 'No hay micrófono disponible.',
      'network': 'Error de conexión.',
      'permission-denied': 'Permiso de micrófono denegado.',
      'bad-grammar': 'Error en el reconocimiento.',
      'service-not-allowed': 'Servicio de reconocimiento no disponible.',
    }
    return errors[errorCode] || `Error: ${errorCode}`
  }

  function startListening() {
    if (!recognition) {
      initializeRecognition()
    }

    if (recognition && !isListening.value) {
      transcript.value = ''
      error.value = ''
      recognition.start()
    }
  }

  function stopListening() {
    if (recognition && isListening.value) {
      recognition.stop()
    }
  }

  function resetTranscript() {
    transcript.value = ''
    error.value = ''
  }

  return {
    transcript: computed(() => transcript.value),
    isListening: computed(() => isListening.value),
    error: computed(() => error.value),
    isSupported: computed(() => isSupported.value),
    startListening,
    stopListening,
    resetTranscript,
  }
}
