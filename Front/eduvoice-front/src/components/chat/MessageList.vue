<template>
  <div class="message-list" role="log" aria-live="polite" aria-relevant="additions">
    <template v-for="message in messages" :key="message.id">
      <UserMessage
        v-if="message.role === 'user'"
        :text="message.text"
        :time="message.time"
      />
      <AssistantMessage
        v-else
        :text="message.text"
        :audio-url="message.audioUrl"
        :time="message.time"
      />
    </template>
  </div>
</template>

<script setup>
import UserMessage from './UserMessage.vue'
import AssistantMessage from './AssistantMessage.vue'

defineProps({
  messages: { type: Array, default: () => [] },
})
</script>

<style src="./MessageList.css"></style>
