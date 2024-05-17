<template>
  <div class="data-height flex w-full gap-4 h-screen">
    <div class="w-1/5 bg-slate-200 flex flex-col">
      <div>
        <input type="search" placeholder="Search..." class="p-1 w-full" />
      </div>
      <div class="overflow-y-auto p-1">
        <TreeNode v-for="root in roots" :taxon="root" :depth="0"></TreeNode>
      </div>
    </div>
    <div class="w-4/5 bg-slate-500"></div>
  </div>
</template>

<script setup>
import TreeNode from './TreeNode.vue';
import axios from 'axios';
import { ref } from 'vue';

const roots = ref([]);

// retrieve the root taxa from the API
axios
  .get('/api/taxon/roots')
  .then((response) => roots.value.push(...response.data));
</script>

<style scoped>
.data-height {
  height: calc(100vh - var(--nav-height) - var(--foot-height));
}
</style>
