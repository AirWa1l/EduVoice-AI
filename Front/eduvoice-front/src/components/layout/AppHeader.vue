<template>
  <header class="app-header">
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
    </div>
  </header>
</template>

<script setup>
import logoUrl from '../../assets/logo.png'
</script>

<style src="./AppHeader.css"></style>
