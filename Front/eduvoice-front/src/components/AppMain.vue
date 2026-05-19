<template>
  <div class="app-shell">
    <AppHeader />

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

const {
  messages,
  draft,
  suggestions,
  isEmpty,
  isRecording,
  isLoading,
  hasError,
  errorMessage,
  applySuggestion,
  toggleRecording,
  sendMessage,
  dismissError,
} = useConversationUI()
</script>

<style src="../styles/app.css"></style>
