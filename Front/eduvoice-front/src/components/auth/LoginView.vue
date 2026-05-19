<template>
  <div class="login-view gradient-bg">
    <div class="gradient-bg__glow gradient-bg__glow--one" aria-hidden="true" />
    <div class="gradient-bg__glow gradient-bg__glow--two" aria-hidden="true" />

    <section class="login-view__card gradient-bg__content" aria-labelledby="login-title">
      <div class="login-view__brand">
        <div class="login-view__logo-wrap">
          <img class="login-view__logo" :src="logoUrl" alt="Logo de EduVoice" />
        </div>
        <h1 id="login-title" class="login-view__title">EduVoice</h1>
        <p class="login-view__subtitle">
          Tu asistente de voz para orientación académica universitaria
        </p>
      </div>

      <div id="google-signin-button" class="login-view__google-container"></div>

      <p class="login-view__note">
        Accede con tu cuenta institucional para comenzar a conversar con el asistente.
      </p>
    </section>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import logoUrl from '../../assets/logo.png'
import { useGoogleAuth } from '../../composables/useGoogleAuth.js'

defineEmits(['login'])

const { renderSignInButton, isInitialized } = useGoogleAuth()

watch(isInitialized, (newVal) => {
  if (newVal) {
    console.log('Google Auth initialized, rendering button')
    // Esperar un tick para asegurar que el DOM esté listo
    setTimeout(() => {
      renderSignInButton('google-signin-button')
    }, 100)
  }
})

onMounted(() => {
  // Si ya está inicializado
  if (isInitialized.value) {
    console.log('Already initialized, rendering button immediately')
    renderSignInButton('google-signin-button')
  }
})
</script>

<style src="./LoginView.css"></style>
