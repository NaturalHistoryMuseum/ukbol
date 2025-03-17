<template>
  <div class="bg-slate-200 flex flex-col text-sm">
    <input
      v-model="search"
      type="search"
      placeholder="Search..."
      class="p-1 border-2 px-4 mx-2 border-b-1 border-gray-500 my-2 rounded-md"
    />
    <div v-if="suggestions.length > 0">
      <ul>
        <li
          v-for="suggestion in suggestions"
          :key="suggestion.name"
          class="p-2 border-black cursor-pointer"
        >
          <router-link
            :to="{ name: 'data', params: { taxonId: suggestion.id } }"
            class="flex justify-between"
            @click="clearSearch"
          >
            <span>{{ suggestion.name }}</span>
            <span>{{ suggestion.rank }}</span>
          </router-link>
        </li>
      </ul>
    </div>

    <ul v-show="suggestions.length === 0" class="overflow-y-auto p-1 relative">
      <Spinner :loading="roots.length === 0"></Spinner>
      <TreeNode
        class="pl-2"
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
import { onMounted, ref, toRef, watch } from 'vue';
import Spinner from '../Spinner.vue';
import { getRoots, getSuggestions, getTaxonParents } from '../../lib/api.js';

const props = defineProps(['taxonId']);
const search = ref('');
const suggestions = ref([]);
const roots = ref([]);
const rootRefs = ref([]);
const taxonId = toRef(props, 'taxonId');

async function setRoots() {
  roots.value = await getRoots();
}

async function focus() {
  if (!taxonId.value) {
    return;
  }
  // get the taxa's parent IDs
  const parentIds = await getTaxonParents(taxonId.value);
  // create a set containing the parent IDs and the actual taxonID
  const targetIds = new Set([taxonId.value, ...parentIds]);
  for (const rootRef of rootRefs.value) {
    await rootRef.focus(targetIds);
  }
}

function clearSearch() {
  search.value = '';
  suggestions.value = [];
}

async function updateSuggestions() {
  suggestions.value = await getSuggestions(search.value, 10);
}

watch(search, async () => {
  if (!!search.value) {
    await updateSuggestions();
  } else {
    suggestions.value = [];
  }
});

watch(taxonId, async () => {
  await focus();
});

onMounted(async () => {
  await setRoots();
  await focus();
});
</script>

<style scoped></style>
