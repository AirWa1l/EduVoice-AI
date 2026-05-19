<template>
  <div class="listening-banner" role="status" aria-live="polite">
    <span class="listening-banner__mic" aria-hidden="true">
      <IconMic :size="22" />
    </span>

    <div class="listening-banner__text">
      <strong>Escuchando...</strong>
      <span>Habla claramente tu pregunta</span>
    </div>

    <div class="listening-banner__visualizer" aria-hidden="true">
      <span />
      <span />
      <span />
      <span />
    </div>
  </div>
</template>

<script setup>
import IconMic from '../icons/IconMic.vue'
</script>

<style src="./ListeningBanner.css"></style>
