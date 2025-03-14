<template>
  <div class="data-height flex w-full">
    <Sidebar class="w-1/4 xl:w-1/5" :taxon-id="taxonId"></Sidebar>
    <div class="w-3/4 xl:w-4/5">
      <div
        v-if="!taxonId"
        class="p-4 h-full text-lg text-center content-center"
      >
        Search or select a name from the tree to the left to get started
      </div>
      <SpeciesView v-else :taxon-id="taxonId" :key="taxonId"></SpeciesView>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '../data/Sidebar.vue';
import SpeciesView from '../data/SpeciesView.vue';
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// Gillmeria Ochrodactyla NHMSYS0021142899 something uk with syns
// Adaina Microdactyla NHMSYS0021142957 also has some uk things
// gammarus fossarum NHMSYS0021164674
// homo sapiens NHMSYS0000376773
const taxonId = ref(route.params.taxonId);

watch(
  () => route.params.taxonId,
  (newTaxonId, oldTaxonId) => {
    taxonId.value = newTaxonId;
  },
);
</script>

<style scoped>
.data-height {
  height: calc(100vh - var(--nav-height) - var(--foot-height));
}
</style>
