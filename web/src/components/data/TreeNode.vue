<template>
  <li class="relative">
    <div @click="onClick" class="cursor-pointer select-none">
      <span class="pr-1.5" :class="nameStyles">{{ taxon.name }}</span>
      <FontAwesomeIcon v-if="!!icon" :icon="icon"></FontAwesomeIcon>
      <Spinner :loading="state === State.Loading"></Spinner>
    </div>

    <template v-if="hasChildren && state === State.Expanded">
      <ul class="relative">
        <TreeNode
          v-for="child in children"
          :key="child.id"
          :taxon="child"
        ></TreeNode>
      </ul>
    </template>
  </li>
</template>

<script setup>
import { ref, computed } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faSquareMinus, faSquarePlus } from '@fortawesome/free-solid-svg-icons';
import Spinner from '../Spinner.vue';
import axios from 'axios';

const State = Object.freeze({
  Leaf: 'Leaf',
  Expanded: 'Expanded',
  Collapsed: 'Collapsed',
  Loading: 'Loading',
});

const { taxon } = defineProps(['taxon']);

// setup some constant values
const hasChildren = taxon.children.length > 0;
const nameStyles = ['capitalize'];
if (['genus', 'species', 'subspecies', 'variety'].includes(taxon.rank)) {
  nameStyles.push('italic');
}

// setup some reactive values
const state = ref(hasChildren ? State.Collapsed : State.Leaf);
const children = ref([]);
const icon = computed(() => {
  switch (state.value) {
    case State.Expanded:
      return faSquareMinus;
    case State.Collapsed:
      return faSquarePlus;
    default:
      return null;
  }
});

async function onClick() {
  console.log(`Selected ${taxon.name} [${taxon.rank}] ${taxon.id}`);

  switch (state.value) {
    case State.Leaf:
      // if it's a species, change the data view
      break;
    case State.Loading:
      // we're loading child data, ignore this request
      break;
    case State.Expanded:
      // collapse the tree
      state.value = State.Collapsed;
      break;
    case State.Collapsed:
      state.value = State.Loading;
      if (hasChildren && children.value.length === 0) {
        try {
          const loadedChildren = (
            await axios.get(`/api/taxon/${taxon.id}/children`)
          ).data;
          children.value.push(...loadedChildren);
        } catch (error) {
          console.error(error);
          state.value = State.Collapsed;
        }
      }
      state.value = State.Expanded;
      break;
  }
}
</script>

<style scoped>
/* h/t https://two-wrongs.com/draw-a-tree-structure-with-only-css.html */
ul {
  list-style: none;
  padding-left: 32px;
}

li::before,
li::after {
  content: '';
  position: absolute;
  left: -12px;
}

li::before {
  border-top: 1px solid #000;
  top: 9px;
  width: 8px;
  height: 0;
}

li::after {
  border-left: 1px solid #000;
  height: 100%;
  width: 0;
  top: 2px;
}

ul > li:last-child::after {
  height: 8px;
}
</style>
