<template>
  <svg
    class="icon"
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="currentColor"
    aria-hidden="true"
  >
    <path d="M8 5v14l11-7z" />
  </svg>
</template>

<script setup>
defineProps({
  size: { type: [Number, String], default: 18 },
})
</script>
