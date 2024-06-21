<template>
  <div class="bg-slate-200 flex flex-col">
    <TaxonSearch></TaxonSearch>

    <ul class="overflow-y-auto p-1 relative">
      <Spinner :loading="roots.length === 0"></Spinner>
      <TreeNode
        v-for="taxon in roots"
        :key="taxon.id"
        :taxon="taxon"
        ref="rootRefs"
      >
      </TreeNode>
    </ul>
  </div>
</template>

<script setup>
import TreeNode from './TreeNode.vue';
import axios from 'axios';
import { onMounted, ref, toRef, watch } from 'vue';
import Spinner from '../Spinner.vue';
import TaxonSearch from './TaxonSearch.vue';

const roots = ref([]);
const rootRefs = ref([]);
const props = defineProps(['taxonId']);
const taxonId = toRef(props, 'taxonId');

async function setRoots() {
  roots.value = (await axios.get('/api/taxon/roots')).data;
}

async function focus() {
  if (!taxonId.value) {
    return;
  }
  // get the taxa's parent IDs
  const parentIds = (await axios.get(`/api/taxon/${taxonId.value}/parents`))
    .data;
  // create a set containing the parent IDs and the actual taxonID
  const targetIds = new Set([taxonId.value, ...parentIds]);
  for (const rootRef of rootRefs.value) {
    await rootRef.focus(targetIds);
  }
}

onMounted(async () => {
  await setRoots();
  await focus();
});

watch(taxonId, async () => {
  await focus();
});
</script>

<style scoped></style>
