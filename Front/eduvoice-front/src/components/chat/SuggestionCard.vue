<template>
  <button class="suggestion-card" type="button" @click="$emit('select', text)">
    {{ text }}
  </button>
</template>

<script setup>
defineProps({
  text: { type: String, required: true },
})

defineEmits(['select'])
</script>

<style src="./SuggestionCard.css"></style>
