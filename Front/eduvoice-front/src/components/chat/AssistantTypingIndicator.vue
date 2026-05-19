<template>
  <article class="assistant-typing" role="status" aria-live="polite" aria-label="El asistente está escribiendo">
    <AssistantAvatar />

    <div class="assistant-typing__bubble" aria-hidden="true">
      <span class="assistant-typing__dot" />
      <span class="assistant-typing__dot" />
      <span class="assistant-typing__dot" />
    </div>
  </article>
</template>

<script setup>
import AssistantAvatar from './AssistantAvatar.vue'
</script>

<style src="./AssistantTypingIndicator.css"></style>
