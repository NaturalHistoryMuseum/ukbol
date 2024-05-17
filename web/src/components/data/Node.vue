<template>
  <ul>
    <li>
      <div
        @click="onClick"
        class="cursor-pointer"
        :style="{ paddingLeft: `${depth * 10}px` }"
      >
        <span class="pr-1.5" :class="nameClass">{{ taxon.name }}</span>
        <FontAwesomeIcon v-if="state !== State.Leaf" :icon="nodeIcon" />
      </div>

      <Node
        v-if="state === State.Expanded"
        v-for="childTaxon in childTaxa"
        :taxon="childTaxon"
        :depth="depth + 1"
      >
      </Node>
    </li>
  </ul>
</template>

<script setup>
import axios from 'axios';
import { computed, ref } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faSquareMinus, faSquarePlus } from '@fortawesome/free-solid-svg-icons';

const State = Object.freeze({
  Leaf: 'Leaf',
  Expanded: 'Expanded',
  Collapsed: 'Collapsed',
});

const { taxon } = defineProps(['taxon', 'depth']);
const childTaxa = ref([]);
const state = ref(taxon.children.length === 0 ? State.Leaf : State.Collapsed);

const nameClass = computed(() => {
  let base = ['capitalize'];
  if (['genus', 'species', 'subspecies', 'variety'].includes(taxon.rank)) {
    base.push('italic');
  }
  return base;
});

const nodeIcon = computed(() => {
  switch (state.value) {
    case State.Expanded:
      return faSquareMinus;
    case State.Collapsed:
      return faSquarePlus;
  }
});

const onClick = () => {
  console.log(`Selected ${taxon.name} [${taxon.rank}] ${taxon.id}`);

  switch (state.value) {
    case State.Leaf:
      // if it's a species, change the data view
      break;
    case State.Expanded:
      // collapse the tree
      state.value = State.Collapsed;
      break;
    case State.Collapsed:
      // expand the tree and load if needed
      if (taxon.children.length > 0 && childTaxa.value.length === 0) {
        axios
          .get(`/api/taxon/${taxon.id}/children`)
          .then((response) => childTaxa.value.push(...response.data))
          .catch(console.log);
      }
      state.value = State.Expanded;
      break;
  }
};
</script>

<style scoped></style>
