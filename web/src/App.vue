<template>
  <div class="w-full">
    <Nav />
    <main class="flex w-full justify-center">
      <RouterView v-slot="{ Component }">
        <component :is="Component" />
      </RouterView>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Nav from './components/Nav.vue';
import Footer from './components/Footer.vue';
</script>

<style scoped>
main {
  min-height: calc(100vh - var(--nav-height) - var(--foot-height));
}
</style>
