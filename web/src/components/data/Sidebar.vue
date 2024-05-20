<template>
  <div class="w-2/5 bg-slate-200 flex flex-col">
    <div>
      <input type="search" placeholder="Search..." class="p-1 w-full" />
    </div>

    <ul class="overflow-y-auto p-1 relative">
      <Suspense v-for="taxon in roots" :key="taxon.id">
        <TreeNode :taxon="taxon"></TreeNode>

        <template #fallback>
          <div>Loading...</div>
        </template>
      </Suspense>
    </ul>
  </div>
</template>

<script setup>
import TreeNode from './TreeNode.vue';
import axios from 'axios';

const roots = (await axios.get('/api/taxon/roots')).data;
</script>

<style scoped></style>
