<template>
  <div class="w-1/5 bg-slate-200 flex flex-col">
    <div>
      <input type="search" placeholder="Search..." class="p-1 w-full" />
    </div>
    <div class="overflow-y-auto p-1">
      <Node v-for="root in roots" :taxon="root" :depth="0"></Node>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import Node from './Node.vue';

const roots = ref([]);

// retrieve the root taxa from the API
axios
  .get('/api/taxon/roots')
  .then((response) => roots.value.push(...response.data));
</script>

<style scoped></style>
