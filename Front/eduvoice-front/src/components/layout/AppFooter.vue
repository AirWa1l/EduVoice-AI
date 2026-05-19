<template>
  <footer class="app-footer">
    <div class="app-footer__row">
      <p class="app-footer__project">
        <IconGraduation class="app-footer__icon" />
        <span>EduVoice · Proyecto de IA para educación universitaria</span>
      </p>

      <p class="app-footer__links">
        <a href="https://github.com" target="_blank" rel="noopener noreferrer" class="app-footer__link">
          <IconGithub />
          <span>GitHub</span>
        </a>
        <span class="app-footer__divider" aria-hidden="true">·</span>
        <span>Hecho con ❤️ para estudiantes</span>
      </p>
    </div>

    <p class="app-footer__disclaimer">
      Este asistente utiliza inteligencia artificial para proporcionar orientación académica.
      Las respuestas son informativas y no reemplazan la asesoría oficial de tu institución.
    </p>
  </footer>
</template>

<script setup>
import IconGithub from '../icons/IconGithub.vue'
import IconGraduation from '../icons/IconGraduation.vue'
</script>

<style src="./AppFooter.css"></style>
