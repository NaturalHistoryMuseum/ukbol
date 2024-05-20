<template>
  <div class="data-height flex w-full gap-4 h-screen">
    <Suspense>
      <Sidebar></Sidebar>

      <template #fallback> Loading... </template>
    </Suspense>
    <MainView></MainView>
  </div>
</template>

<script setup>
import Sidebar from '../data/Sidebar.vue';
import MainView from '../data/MainView.vue';
</script>

<style scoped>
.data-height {
  height: calc(100vh - var(--nav-height) - var(--foot-height));
}
</style>
