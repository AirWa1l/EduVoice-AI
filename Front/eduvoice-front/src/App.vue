<template>
  <LoginView v-if="!isAuthenticated" @login="handleGoogleLogin" />
  <AppMain v-else :user="user" @logout="handleLogout" />
</template>

<script setup>
import LoginView from './components/auth/LoginView.vue'
import AppMain from './components/AppMain.vue'
import { useGoogleAuth } from './composables/useGoogleAuth.js'

const { isAuthenticated, user, handleCredentialResponse, logout } = useGoogleAuth()

function handleGoogleLogin(credentialResponse) {
  handleCredentialResponse(credentialResponse)
}

function handleLogout() {
  logout()
}
</script>
