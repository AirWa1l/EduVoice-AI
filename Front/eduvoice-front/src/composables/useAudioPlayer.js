import { ref, computed } from 'vue'

export function useAudioPlayer() {
  const currentAudioUrl = ref(null)
  const isPlaying = ref(false)
  const audioElement = new Audio()

  // Eventos del elemento de audio
  audioElement.addEventListener('play', () => {
    isPlaying.value = true
  })

  audioElement.addEventListener('pause', () => {
    isPlaying.value = false
  })

  audioElement.addEventListener('ended', () => {
    isPlaying.value = false
  })

  audioElement.addEventListener('error', (err) => {
    console.error('Audio playback error:', err)
    isPlaying.value = false
  })

  /**
   * Play audio from URL
   */
  function playAudio(audioUrl) {
    if (!audioUrl) {
      console.warn('No audio URL provided')
      return
    }

    try {
      currentAudioUrl.value = audioUrl
      audioElement.src = audioUrl
      audioElement.play().catch((err) => {
        console.error('Error playing audio:', err)
      })
    } catch (err) {
      console.error('Error setting up audio:', err)
    }
  }

  /**
   * Stop audio playback
   */
  function stopAudio() {
    audioElement.pause()
    audioElement.currentTime = 0
    isPlaying.value = false
  }

  /**
   * Pause audio
   */
  function pauseAudio() {
    audioElement.pause()
  }

  /**
   * Resume audio
   */
  function resumeAudio() {
    audioElement.play().catch((err) => {
      console.error('Error resuming audio:', err)
    })
  }

  return {
    currentAudioUrl: computed(() => currentAudioUrl.value),
    isPlaying: computed(() => isPlaying.value),
    playAudio,
    stopAudio,
    pauseAudio,
    resumeAudio,
  }
}
