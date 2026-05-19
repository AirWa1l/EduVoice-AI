<template>
  <LoginView v-if="!isAuthenticated" @login="handleLogin" />
  <AppMain v-else />
</template>

<script setup>
import { ref } from 'vue'
import LoginView from './components/auth/LoginView.vue'
import AppMain from './components/AppMain.vue'

const isAuthenticated = ref(false)

function handleLogin() {
  isAuthenticated.value = true
}
</script>
