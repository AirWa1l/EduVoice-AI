<template>
  <section class="chat-view" aria-label="Conversación">
    <ErrorBanner
      v-if="hasError"
      :message="errorMessage"
      @dismiss="$emit('dismiss-error')"
    />

    <ListeningBanner v-if="isRecording" />

    <WelcomeState
      v-if="showWelcome"
      :suggestions="suggestions"
      @select-suggestion="$emit('select-suggestion', $event)"
    />

    <div v-else class="chat-view__thread">
      <MessageList :messages="messages" />
      <AssistantTypingIndicator v-if="isLoading" />
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import WelcomeState from './WelcomeState.vue'
import ListeningBanner from './ListeningBanner.vue'
import ErrorBanner from './ErrorBanner.vue'
import MessageList from './MessageList.vue'
import AssistantTypingIndicator from './AssistantTypingIndicator.vue'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  suggestions: { type: Array, default: () => [] },
  isEmpty: { type: Boolean, default: true },
  isRecording: { type: Boolean, default: false },
  isLoading: { type: Boolean, default: false },
  hasError: { type: Boolean, default: false },
  errorMessage: { type: String, default: '' },
})

defineEmits(['select-suggestion', 'dismiss-error'])

const showWelcome = computed(
  () => props.isEmpty && !props.isRecording && !props.isLoading,
)
</script>

<style src="./ChatView.css"></style>
