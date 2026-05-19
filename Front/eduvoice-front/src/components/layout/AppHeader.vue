<template>
  <header class="app-header">
    <div class="app-header__glow app-header__glow--one" aria-hidden="true" />
    <div class="app-header__glow app-header__glow--two" aria-hidden="true" />

    <div class="app-header__inner">
      <div class="app-header__brand">
        <img class="app-header__logo" :src="logoUrl" alt="Logo de EduVoice" />
        <div class="app-header__titles">
          <h1 class="app-header__title">EduVoice</h1>
          <p class="app-header__subtitle">
            Asistente de voz para orientación académica universitaria
          </p>
        </div>
      </div>

      <div v-if="user" class="app-header__user">
        <img v-if="user.picture" :src="user.picture" :alt="user.name" class="app-header__avatar" />
        <span class="app-header__user-name">{{ user.name }}</span>
        <button class="app-header__logout" @click="handleLogout" title="Cerrar sesión">
          ✕
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import logoUrl from '../../assets/logo.png'

defineProps({
  user: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['logout'])

function handleLogout() {
  emit('logout')
}
</script>

<style src="./AppHeader.css"></style>
