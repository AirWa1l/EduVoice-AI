<template>
  <article class="assistant-message">
    <AssistantAvatar />

    <div class="assistant-message__card">
      <div class="assistant-message__body" v-html="formattedText" />

      <div v-if="audioUrl" class="assistant-message__audio">
        <button
          class="assistant-message__play"
          type="button"
          :aria-label="isPlaying ? 'Pausar audio' : 'Reproducir respuesta en audio'"
          @click="toggleAudio"
        >
          <IconPlay />
          <span>{{ isPlaying ? 'Reproduciendo...' : 'Escuchar respuesta' }}</span>
        </button>
      </div>

      <time v-if="time" class="assistant-message__time" :datetime="time">{{ time }}</time>
    </div>
  </article>
</template>

<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import IconPlay from '../icons/IconPlay.vue'
import AssistantAvatar from './AssistantAvatar.vue'
import { formatMessage } from '../../utils/formatMessage.js'

const props = defineProps({
  text: { type: String, required: true },
  audioUrl: { type: String, default: null },
  time: { type: String, default: '' },
})

const isPlaying = ref(false)
let audioElement = null

const formattedText = computed(() => formatMessage(props.text))

function toggleAudio() {
  if (!props.audioUrl) return

  if (!audioElement) {
    audioElement = new Audio(props.audioUrl)
    audioElement.addEventListener('ended', () => {
      isPlaying.value = false
    })
  }

  if (isPlaying.value) {
    audioElement.pause()
    isPlaying.value = false
    return
  }

  audioElement.play()
  isPlaying.value = true
}

watch(
  () => props.audioUrl,
  () => {
    if (audioElement) {
      audioElement.pause()
      audioElement = null
      isPlaying.value = false
    }
  },
)

onBeforeUnmount(() => {
  if (audioElement) {
    audioElement.pause()
    audioElement = null
  }
})
</script>

<style src="./AssistantMessage.css"></style>
