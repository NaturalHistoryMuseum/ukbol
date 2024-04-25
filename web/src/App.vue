<template>
  <Nav />
  <main class="flex w-screen justify-center pt-5">
    <RouterView />
  </main>
</template>

<script setup lang="ts">
import Nav from './components/Nav.vue';
</script>

<style scoped></style>
