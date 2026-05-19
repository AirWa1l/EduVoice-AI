<template>
  <article class="user-message">
    <div class="user-message__content">
      <p class="user-message__text">{{ text }}</p>
      <time class="user-message__time" :datetime="time">{{ time }}</time>
    </div>
    <span class="user-message__avatar" aria-hidden="true">TÚ</span>
  </article>
</template>

<script setup>
defineProps({
  text: { type: String, required: true },
  time: { type: String, default: '' },
})
</script>

<style src="./UserMessage.css"></style>
