<template>
  <FontAwesomeIcon
    v-if="loading"
    class="spinner"
    :icon="faSpinner"
  ></FontAwesomeIcon>
</template>

<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

const { loading } = defineProps(['loading']);
</script>

<style scoped>
.spinner {
  animation: spinner 1.5s linear infinite;
}

@keyframes spinner {
  to {
    transform: rotate(360deg);
  }
}
</style>
