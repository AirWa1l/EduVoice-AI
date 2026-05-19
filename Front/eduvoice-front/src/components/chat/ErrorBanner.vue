<template>
  <div class="error-banner" role="alert">
    <p class="error-banner__message">{{ message }}</p>
    <button class="error-banner__dismiss" type="button" @click="$emit('dismiss')">
      Cerrar
    </button>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, required: true },
})

defineEmits(['dismiss'])
</script>

<style src="./ErrorBanner.css"></style>
