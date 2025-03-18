<template>
  <table class="w-full table-auto text-md">
    <thead class="sticky top-0 z-10 text-left">
      <tr>
        <th
          v-for="header in headers"
          class="border-b font-bold pl-2 py-4 text-left bg-slate-300"
        >
          {{ header }}
        </th>
      </tr>
    </thead>
    <tbody>
      <template v-if="binSummaries.length > 0">
        <tr
          v-for="binSummary in binSummaries"
          :key="binSummary.bin"
          class="text-left bg-slate-100 even:bg-slate-200"
        >
          <td class="py-2 pl-2">
            <a target="_blank" :href="getBINLink(binSummary)">
              {{ binSummary.bin }}
            </a>
          </td>
          <td class="py-2 pl-2">{{ binSummary.count }}</td>
          <td class="py-2 pl-2">{{ binSummary.uk_count }}</td>
          <td class="py-2 pl-2">
            <p v-for="[name, count] in binSummary.names">
              <span class="italic">{{ capitalise(name) }}</span>
              <span> ({{ count }})</span>
            </p>
          </td>
        </tr>
      </template>
      <template v-else>
        <tr>
          <td :colspan="headers.length" class="text-center pt-6 font-bold">
            No specimens found
          </td>
        </tr>
      </template>
    </tbody>
  </table>
</template>

<script setup>
import { capitalise } from '../../lib/utils.js';

const headers = [
  'BIN URI',
  'Number specimens (all)',
  'Number specimens (UK)',
  'Names in BIN',
];

const { binSummaries } = defineProps(['binSummaries']);

function getBINLink(binSummary) {
  return `https://portal.boldsystems.org/bin/${binSummary.bin}`;
}
</script>

<style scoped></style>
