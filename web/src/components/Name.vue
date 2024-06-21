<template>
  <span :class="styles">{{ capitalise(name) }}</span>
  <template v-if="!!authorship">
    <span>&nbsp;{{ authorship }}</span>
  </template>
</template>

<script setup>
import { capitalise } from '../lib/utils.js';

const { name, authorship, rank } = defineProps(['name', 'authorship', 'rank']);

const styles = [];
const italicRanks = ['genus', 'species', 'subspecies', 'variety'];
if (italicRanks.includes(!rank ? null : rank.toLowerCase())) {
  styles.push('italic');
}
</script>

<style scoped></style>
