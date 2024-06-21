<template>
  <span class="italic">{{ capitalise(name) }}</span>
  <template v-if="!!authorship">
    <span>&nbsp;{{ authorship }}</span>
  </template>
</template>

<script setup>
import { capitalise } from '../lib/utils.js';

const { name, authorship } = defineProps(['name', 'authorship']);
</script>

<style scoped></style>
