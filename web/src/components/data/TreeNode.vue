<template>
  <li class="relative scroll-m-20 whitespace-nowrap text-sm" ref="element">
    <div
      @click="onClick"
      class="cursor-pointer select-none"
      :class="{ 'font-bold': isSelected }"
    >
      <FontAwesomeIcon
        class="pr-2"
        v-if="!!icon"
        :icon="icon"
      ></FontAwesomeIcon>
      <span v-else class="pr-5"></span>
      <Name :name="taxon.name" :rank="taxon.rank"></Name>
      <Spinner class="ml-2" :loading="isLoading"></Spinner>
    </div>

    <template v-if="isExpanded">
      <ul class="relative whitespace-nowrap">
        <TreeNode
          v-for="child in children"
          :key="child.id"
          :taxon="child"
          ref="childRefs"
        ></TreeNode>
      </ul>
    </template>
  </li>
</template>

<script setup>
import { computed, nextTick, ref } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
  faSquareMinus,
  faSquarePlus,
} from '@fortawesome/free-regular-svg-icons';
import Spinner from '../Spinner.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Name from '../Name.vue';

const router = useRouter();

const { taxon } = defineProps(['taxon']);

// setup some constant values
const hasChildren = taxon.children.length > 0;
const nameStyles = [];
if (['genus', 'species', 'subspecies', 'variety'].includes(taxon.rank)) {
  nameStyles.push('italic');
}

// setup some reactive values
// first refs to elements in the template
const element = ref(null);
const childRefs = ref([]);
// next state variables
const isSelected = ref(false);
const isExpanded = ref(false);
const isLoading = ref(false);
// and finally, the node's children
const children = ref([]);

// a computed icon dependent on the current state
const icon = computed(() => {
  if (hasChildren) {
    if (isExpanded.value) {
      return faSquareMinus;
    } else {
      return faSquarePlus;
    }
  } else {
    return null;
  }
});

async function expand() {
  if (!hasChildren) {
    return;
  }

  // we're already loading child data, ignore this request
  if (isLoading.value) {
    return;
  }

  if (children.value.length === 0) {
    isLoading.value = true;
    try {
      const loadedChildren = (
        await axios.get(`/api/taxon/${taxon.id}/children`)
      ).data;
      children.value.push(...loadedChildren);
    } catch (error) {
      console.error(error);
    } finally {
      isLoading.value = false;
    }
  }
  isExpanded.value = true;
}

function collapse() {
  isExpanded.value = false;
}

function select() {
  isSelected.value = true;
}

function deselect() {
  isSelected.value = false;
}

async function onClick() {
  if (isExpanded.value) {
    collapse();
  } else {
    await expand();
    if (taxon.rank === 'species') {
      select();
      await router.push({ name: 'data', params: { taxonId: taxon.id } });
    }
  }
}

async function focus(targetIds) {
  if (targetIds.has(taxon.id)) {
    select();
    await expand();
    await nextTick(() => {
      element.value.scrollIntoView({ block: 'start', behavior: 'smooth' });
    });
  } else {
    deselect();
  }
  for (const childRef of childRefs.value) {
    await childRef.focus(targetIds);
  }
}

defineExpose({ focus });
</script>

<style scoped>
/* h/t https://two-wrongs.com/draw-a-tree-structure-with-only-css.html */
ul {
  list-style: none;
  padding-left: 14px;
}

li::before,
li::after {
  content: '';
  position: absolute;
  left: -12px;
}

li::before {
  border-top: 1px solid #94a3b8;
  top: 9px;
  width: 8px;
  height: 0;
}

li::after {
  border-left: 1px solid #94a3b8;
  height: 100%;
  width: 0;
  top: 2px;
}

ul > li:last-child::after {
  height: 7px;
}
</style>
