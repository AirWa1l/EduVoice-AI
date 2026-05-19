<template>
  <div class="app-shell">
    <AppHeader :user="user" @logout="handleLogout" />

    <main class="app-shell__main">
      <ChatView
        :messages="messages"
        :suggestions="suggestions"
        :is-empty="isEmpty"
        :is-recording="isRecording"
        :is-loading="isLoading"
        :has-error="hasError"
        :error-message="errorMessage"
        @select-suggestion="applySuggestion"
        @dismiss-error="dismissError"
      />

      <InputPanel
        v-model="draft"
        :is-recording="isRecording"
        :is-loading="isLoading"
        @toggle-record="toggleRecording"
        @send="sendMessage"
      />
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from './layout/AppHeader.vue'
import AppFooter from './layout/AppFooter.vue'
import ChatView from './chat/ChatView.vue'
import InputPanel from './input/InputPanel.vue'
import { useConversationUI } from '../composables/useConversationUI.js'
import { computed } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['logout'])

// Obtener el ID del usuario autenticado
const userId = computed(() => props.user?.id || null)

const {
  messages,
  draft,
  suggestions,
  isEmpty,
  isRecording,
  isLoading,
  hasError,
  errorMessage,
  isPlaying,
  applySuggestion,
  toggleRecording,
  sendMessage,
  dismissError,
} = useConversationUI(userId.value)

function handleLogout() {
  emit('logout')
}
</script>

<style src="../styles/app.css"></style>
