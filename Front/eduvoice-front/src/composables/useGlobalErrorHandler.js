import { ref } from 'vue'

const globalError = ref('')
let listenersInstalled = false

function normalizeErrorMessage(error, fallback) {
  if (!error) {
    return fallback
  }

  if (typeof error === 'string') {
    return error
  }

  if (error instanceof Error && error.message) {
    return error.message
  }

  if (typeof error === 'object' && error.message) {
    return error.message
  }

  return fallback
}

function setGlobalError(error) {
  globalError.value = normalizeErrorMessage(
    error,
    'Se produjo un error inesperado. Intenta recargar la página.',
  )
}

function clearGlobalError() {
  globalError.value = ''
}

function installGlobalErrorHandlers(app) {
  if (listenersInstalled || typeof window === 'undefined') {
    return
  }

  listenersInstalled = true

  app.config.errorHandler = (error, instance, info) => {
    console.error('Vue application error:', error, info, instance)
    setGlobalError(error)
  }

  window.addEventListener('error', (event) => {
    setGlobalError(event.error || event.message)
  })

  window.addEventListener('unhandledrejection', (event) => {
    setGlobalError(event.reason)
  })
}

export { globalError, clearGlobalError, installGlobalErrorHandlers, setGlobalError }