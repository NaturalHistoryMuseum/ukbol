<template>
  <div>
    <input
      v-model="search"
      type="search"
      placeholder="Search..."
      class="p-1 w-full"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';

const search = ref('');
</script>

<style scoped></style>
