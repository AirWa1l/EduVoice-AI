<template>
  <section class="input-panel" aria-label="Enviar consulta">
    <div class="input-panel__row">
      <button
        class="input-panel__record"
        :class="{ 'input-panel__record--active': isRecording }"
        type="button"
        :disabled="isLoading"
        :aria-pressed="isRecording"
        @click="$emit('toggle-record')"
      >
        <IconStop v-if="isRecording" />
        <IconMic v-else />
        <span>{{ isRecording ? 'Detener' : 'Grabar' }}</span>
      </button>

      <label class="input-panel__field">
        <span class="sr-only">Escribe tu pregunta</span>
        <textarea
          :value="modelValue"
          class="input-panel__textarea"
          rows="1"
          placeholder="O escribe tu pregunta aquí..."
          :disabled="isLoading"
          @input="onInput"
          @keydown="onKeydown"
        />
      </label>

      <button
        class="input-panel__send"
        type="button"
        aria-label="Enviar consulta"
        :disabled="isLoading || !modelValue.trim()"
        @click="$emit('send')"
      >
        <IconSend />
      </button>
    </div>

    <p class="input-panel__hint">
      Presiona Enter para enviar, Shift + Enter para nueva línea
    </p>
  </section>
</template>

<script setup>
import IconMic from '../icons/IconMic.vue'
import IconStop from '../icons/IconStop.vue'
import IconSend from '../icons/IconSend.vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  isRecording: { type: Boolean, default: false },
  isLoading: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'toggle-record', 'send'])

function onInput(event) {
  emit('update:modelValue', event.target.value)
}

function onKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    if (!props.isLoading && props.modelValue.trim()) {
      emit('send')
    }
  }
}
</script>

<style src="./InputPanel.css"></style>
