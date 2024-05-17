<template>
  <ul>
    <li>
      <div
        @click="onClick"
        class="cursor-pointer"
        :style="{ paddingLeft: `${depth * 10}px` }"
      >
        <span :class="nameClass">{{ taxon.name }}</span>
        <FontAwesomeIcon
          v-if="taxon.children.length > 0"
          :icon="faCaretRight"
        />
      </div>

      <Node
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
import { faCaretRight } from '@fortawesome/free-solid-svg-icons';

const { taxon } = defineProps(['taxon', 'depth']);
const childTaxa = ref([]);

const nameClass = computed(() => {
  let base = ['capitalize'];
  if (['genus', 'species', 'subspecies', 'variety'].includes(taxon.rank)) {
    base.push('italic');
  }
  return base;
});

const onClick = () => {
  console.log(`Selected ${taxon.name} [${taxon.rank}] ${taxon.id}`);
  if (taxon.children.length > 0) {
    if (childTaxa.value.length === 0) {
      axios
        .get(`/api/taxon/${taxon.id}/children`)
        .then((response) => childTaxa.value.push(...response.data))
        .catch(console.log);
    }
  }
};
</script>

<style scoped></style>
