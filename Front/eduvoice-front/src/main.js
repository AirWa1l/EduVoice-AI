import { createApp } from 'vue'
import App from './App.vue'
import './styles/main.css'
import { installGlobalErrorHandlers } from './composables/useGlobalErrorHandler.js'

const app = createApp(App)

installGlobalErrorHandlers(app)

app.mount('#app')
