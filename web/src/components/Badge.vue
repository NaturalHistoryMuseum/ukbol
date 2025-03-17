<template>
  <div class="text-xs">
    <span class="p-1.5 pl-2 rounded-l-md text-white bg-slate-500">{{
      label
    }}</span>
    <span class="p-1.5 pr-2 rounded-r-md text-white" :class="[colour]">{{
      value
    }}</span>
  </div>
</template>

<script setup>
const { label, value, colour } = defineProps(['label', 'value', 'colour']);
</script>

<style scoped>
.cyan {
  @apply bg-cyan-600;
}

.orange {
  @apply bg-orange-400;
}

.green {
  @apply bg-green-600;
}

.purple {
  @apply bg-purple-500;
}
</style>
