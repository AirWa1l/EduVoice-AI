<template>
  <div class="login-view gradient-bg">
    <div class="gradient-bg__glow gradient-bg__glow--one" aria-hidden="true" />
    <div class="gradient-bg__glow gradient-bg__glow--two" aria-hidden="true" />

    <section class="login-view__card gradient-bg__content" aria-labelledby="login-title">
      <div class="login-view__brand">
        <div class="login-view__logo-wrap">
          <img class="login-view__logo" :src="logoUrl" alt="Logo de EduVoice" />
        </div>
      </div>

      <div class="login-view__copy">
        <h1 id="login-title" class="login-view__title">EduVoice</h1>
        <p class="login-view__subtitle">
          Tu asistente de voz para orientación académica universitaria
        </p>
      </div>

      <div class="login-view__google-shell">
        <div id="google-signin-button" class="login-view__google-container"></div>
      </div>

      <p class="login-view__note">
        Accede con tu cuenta institucional para comenzar a conversar con el asistente.
      </p>
    </section>
  </div>
</template>

<script setup>
import { nextTick, onMounted, watch } from 'vue'
import logoUrl from '../../assets/logo.png'
import { useGoogleAuth } from '../../composables/useGoogleAuth.js'

const { renderSignInButton, isInitialized } = useGoogleAuth()

async function renderGoogleButton() {
  await nextTick()
  renderSignInButton('google-signin-button')
}

watch(isInitialized, (newVal) => {
  if (newVal) {
    renderGoogleButton()
  }
})

onMounted(() => {
  if (isInitialized.value) {
    renderGoogleButton()
  }
})
</script>

<style src="./LoginView.css"></style>
