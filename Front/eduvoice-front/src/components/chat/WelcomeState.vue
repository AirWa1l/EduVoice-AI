<template>
  <section class="welcome-state" aria-label="Bienvenida">
    <div class="welcome-state__hero">
      <div class="welcome-state__icon-wrap" aria-hidden="true">
        <IconMessage />
      </div>
      <h2 class="welcome-state__title">¡Bienvenido a EduVoice!</h2>
      <p class="welcome-state__description">
        Tu asistente inteligente para orientación académica universitaria. Pregunta lo que
        necesites sobre tu carrera, materias o planificación.
      </p>
    </div>

    <div class="welcome-state__hints">
      <p class="welcome-state__hint">
        <IconMic class="welcome-state__hint-icon" :size="18" />
        <span>Haz clic en el micrófono para hablar</span>
      </p>
      <p class="welcome-state__hint">
        <span class="welcome-state__hint-letter" aria-hidden="true">T</span>
        <span>O escribe tu pregunta</span>
      </p>
    </div>

    <div class="welcome-state__grid">
      <SuggestionCard
        v-for="item in suggestions"
        :key="item"
        :text="item"
        @select="$emit('select-suggestion', $event)"
      />
    </div>
  </section>
</template>

<script setup>
import IconMessage from '../icons/IconMessage.vue'
import IconMic from '../icons/IconMic.vue'
import SuggestionCard from './SuggestionCard.vue'

defineProps({
  suggestions: { type: Array, default: () => [] },
})

defineEmits(['select-suggestion'])
</script>

<style src="./WelcomeState.css"></style>
