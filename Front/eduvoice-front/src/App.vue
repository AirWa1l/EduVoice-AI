<template>
  <ErrorBanner
    v-if="globalError"
    :message="globalError"
    @dismiss="clearGlobalError"
  />
  <LoginView v-if="!isAuthenticated" @login="handleGoogleLogin" />
  <AppMain v-else :user="user" @logout="handleLogout" />
</template>

<script setup>
import LoginView from './components/auth/LoginView.vue'
import AppMain from './components/AppMain.vue'
import ErrorBanner from './components/chat/ErrorBanner.vue'
import { useGoogleAuth } from './composables/useGoogleAuth.js'
import { clearGlobalError, globalError } from './composables/useGlobalErrorHandler.js'

const { isAuthenticated, user, handleCredentialResponse, logout } = useGoogleAuth()

function handleGoogleLogin(credentialResponse) {
  handleCredentialResponse(credentialResponse)
}

function handleLogout() {
  logout()
}
</script>
