import { ref, computed, onMounted } from 'vue'

const isAuthenticated = ref(false)
const user = ref(null)
const token = ref(null)
const isInitialized = ref(false)

export function useGoogleAuth() {
  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID

  console.log('Client ID:', clientId)

  // Cargar Google SDK
  function initializeGoogleSDK() {
    return new Promise((resolve) => {
      // Verificar si ya está cargado
      if (window.google) {
        console.log('Google SDK already loaded')
        resolve()
        return
      }

      console.log('Loading Google SDK...')
      // Crear script tag
      const script = document.createElement('script')
      script.src = 'https://accounts.google.com/gsi/client'
      script.async = true
      script.defer = true
      script.onload = () => {
        console.log('Google SDK loaded successfully')
        resolve()
      }
      script.onerror = () => {
        console.error('Failed to load Google SDK')
        resolve()
      }
      document.head.appendChild(script)
    })
  }

  // Inicializar Google Sign-In
  async function initialize() {
    try {
      await initializeGoogleSDK()

      if (!window.google) {
        console.error('Google SDK is not available')
        return
      }

      console.log('Initializing Google Sign-In with Client ID:', clientId)
      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: handleCredentialResponse,
      })
      isInitialized.value = true
      console.log('Google Sign-In initialized')
    } catch (error) {
      console.error('Error initializing Google Sign-In:', error)
    }
  }

  // Callback cuando el usuario se autentica
  function handleCredentialResponse(response) {
    console.log('Credential response received')
    try {
      const payload = JSON.parse(atob(response.credential.split('.')[1]))

      user.value = {
        id: payload.sub,
        email: payload.email,
        name: payload.name,
        picture: payload.picture,
      }

      token.value = response.credential
      isAuthenticated.value = true

      // Guardar en localStorage
      localStorage.setItem('auth_token', response.credential)
      localStorage.setItem('user', JSON.stringify(user.value))
      console.log('User authenticated:', user.value)
    } catch (error) {
      console.error('Error processing credential response:', error)
    }
  }

  // Renderizar botón de Google Sign-In
  function renderSignInButton(elementId) {
    if (window.google && isInitialized.value) {
      console.log('Rendering Google Sign-In button')
      window.google.accounts.id.renderButton(document.getElementById(elementId), {
        theme: 'filled_blue',
        size: 'large',
        text: 'signin_with',
      })
    } else {
      console.warn('Google SDK not ready for rendering button')
    }
  }

  // Logout
  function logout() {
    if (window.google) {
      window.google.accounts.id.disableAutoSelect()
    }
    isAuthenticated.value = false
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
    console.log('User logged out')
  }

  // Restaurar sesión desde localStorage
  function restoreSession() {
    const savedToken = localStorage.getItem('auth_token')
    const savedUser = localStorage.getItem('user')

    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = JSON.parse(savedUser)
      isAuthenticated.value = true
      console.log('Session restored from localStorage')
      return true
    }
    return false
  }

  onMounted(() => {
    initialize()
    restoreSession()
  })

  return {
    isAuthenticated: computed(() => isAuthenticated.value),
    user: computed(() => user.value),
    token: computed(() => token.value),
    isInitialized: computed(() => isInitialized.value),
    renderSignInButton,
    logout,
    handleCredentialResponse,
    initialize,
  }
}
