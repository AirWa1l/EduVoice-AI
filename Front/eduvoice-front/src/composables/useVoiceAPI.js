import { ref } from 'vue'

export function useVoiceAPI() {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const isProcessing = ref(false)
  const error = ref(null)

  /**
   * Process voice input through backend API
   * Sends text query and receives LLM response + audio
   */
  async function processVoice(text, userId, sessionId) {
    if (!text || !text.trim()) {
      error.value = 'El texto no puede estar vacío'
      return null
    }

    isProcessing.value = true
    error.value = null

    try {
      const endpoint = `${apiUrl}/api/voice/process`
      
      console.log('Calling backend API:', endpoint)
      console.log('Payload:', { text, user_id: userId, session_id: sessionId })

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text.trim(),
          user_id: userId,
          session_id: sessionId,
        }),
      })

      // Si no es 2xx, lanzar error
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `API error: ${response.status}`)
      }

      const data = await response.json()

      console.log('API Response:', data)

      return {
        textResponse: data.text_response,
        audioUrl: data.audio_url,
        latencyMs: data.latency_ms,
        status: data.status,
      }
    } catch (err) {
      console.error('Voice API Error:', err)
      error.value = err.message || 'Error al procesar la solicitud'
      return null
    } finally {
      isProcessing.value = false
    }
  }

  /**
   * Check health of backend services
   */
  async function checkHealth() {
    try {
      const endpoint = `${apiUrl}/api/voice/health`
      const response = await fetch(endpoint)
      
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`)
      }

      const data = await response.json()
      console.log('Health check:', data)
      return data
    } catch (err) {
      console.error('Health check error:', err)
      return { status: 'unhealthy', error: err.message }
    }
  }

  return {
    isProcessing,
    error,
    processVoice,
    checkHealth,
  }
}
