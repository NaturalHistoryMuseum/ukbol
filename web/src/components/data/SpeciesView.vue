<template>
  <div class="bg-slate-100 flex flex-col h-full">
    <div v-if="status" class="place-self-center mt-20 text-center">
      <Spinner class="text-3xl" :loading="true"></Spinner>
      <p class="pt-4 text-sm italic">{{ status }}</p>
    </div>
    <template v-else>
      <div class="flex">
        <div class="grow p-4">
          <div class="text-2xl font-bold">
            <Name
              :name="taxon.name"
              :authorship="taxon.authorship"
              :rank="taxon.rank"
            >
            </Name>
          </div>
          <div class="flex gap-2 items-center pt-2 pb-2">
            <a
              :href="`https://species.nbnatlas.org/species/${taxon.id}`"
              target="_blank"
            >
              <Badge label="UKSI TVK" :value="taxon.id" colour="cyan"></Badge>
            </a>
            <Badge
              label="Rank"
              :value="capitalise(taxon.rank)"
              colour="purple"
            ></Badge>
            <Badge
              label="Specimens"
              :value="specimenCount"
              colour="orange"
            ></Badge>
            <Badge
              label="Clusters"
              :value="binGroups.length"
              colour="green"
            ></Badge>
          </div>
          <div v-if="!!gbifTaxon" class="text-lg">
            GBIF accepted name:
            <a
              :href="`https://www.gbif.org/species/${gbifTaxon.usageKey}`"
              target="_blank"
            >
              <Name :name="gbifTaxon.scientificName" :rank="taxon.rank"></Name>
            </a>
          </div>
          <div v-else class="italic">No GBIF name match found</div>
          <div v-if="taxon.synonyms.length > 0">
            UKSI Synonyms:
            <span
              v-for="synonym in taxon.synonyms"
              class="after:content-[',_'] last:after:content-none"
            >
              <Name
                :name="synonym.name"
                :authorship="synonym.authorship"
                :rank="synonym.rank"
              ></Name>
            </span>
          </div>
        </div>
        <div
          class="flex-none p-4 flex flex-col gap-4 items-end justify-between"
        >
          <div>
            <a v-if="!!phylopicData" :href="phylopicData.link" target="_blank">
              <img
                class="w-16 h-16"
                :src="phylopicData.url"
                alt="phylopic image"
              />
            </a>
          </div>
          <div class="my-2">
            <a
              v-if="binGroups.length > 0"
              class="border-2 text-white p-2 border-black bg-slate-500 rounded-md hover:text-slate-100"
              :href="downloadUrl"
            >
              Download as CSV
              <FontAwesomeIcon
                class="pl-2"
                :icon="faDownload"
              ></FontAwesomeIcon>
            </a>
          </div>
        </div>
      </div>
      <div class="px-4 pb-4 overflow-y-auto">
        <table class="w-full table-auto text-md">
          <thead class="sticky top-0 z-10 text-left">
            <tr>
              <th
                v-for="header in headers"
                class="border-b font-medium pl-2 py-4 text-left bg-slate-300"
              >
                {{ header }}
              </th>
            </tr>
          </thead>
          <tbody>
            <template v-if="binGroups.length > 0">
              <tr
                v-for="binGroup in binGroups"
                :key="binGroup.bin"
                class="text-left bg-slate-100 even:bg-slate-200"
              >
                <td class="py-2 pl-2">
                  <a
                    target="_blank"
                    :href="`https://doi.org/10.5883/${binGroup.bin}`"
                  >
                    {{ binGroup.bin }}
                  </a>
                </td>
                <td class="py-2 pl-2">{{ binGroup.count }}</td>
                <td class="py-2 pl-2">{{ binGroup.ukCount }}</td>
                <td class="py-2 pl-2">
                  {{ getNonSpeciesNames(binGroup.names) }}
                </td>
              </tr>
            </template>
            <template v-else>
              <tr>
                <td
                  :colspan="headers.length"
                  class="text-center pt-6 font-bold"
                >
                  No specimens found
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<script setup>
import Name from '../Name.vue';
import Badge from '../Badge.vue';
import { capitalise } from '../../lib/utils.js';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faDownload } from '@fortawesome/free-solid-svg-icons';
import {
  buildDownloadUrl,
  getGBIFData,
  getPhylopicData,
  getTaxon,
  getTaxonBins,
} from '../../lib/api.js';
import { computed, ref, watchEffect } from 'vue';
import Spinner from '../Spinner.vue';

const headers = [
  'BIN',
  'Number specimens (all)',
  'Number specimens (UK)',
  'Different names in BIN',
];
const props = defineProps(['taxonId']);
const status = ref('Loading...');
const taxon = ref(null);
const gbifTaxon = ref(null);
const phylopicData = ref(null);
const binGroups = ref([]);
const specimenCount = ref(0);

watchEffect(async () => {
  status.value = 'Loading taxon data...';
  taxon.value = await getTaxon(props.taxonId);
  // update the page title with the taxon name
  document.title = `UKBoL - ${capitalise(taxon.value.name)}`;
  status.value = 'Loading GBIF data...';
  gbifTaxon.value = await getGBIFData(taxon.value.name, taxon.value.rank);
  status.value = 'Loading icon data...';
  phylopicData.value = !gbifTaxon.value
    ? null
    : await getPhylopicData(gbifTaxon.value);
  status.value = 'Loading BOLD data...';
  binGroups.value = await getTaxonBins(props.taxonId);
  specimenCount.value = binGroups.value.reduce(
    (acc, bin) => acc + bin.count,
    0,
  );
  status.value = '';
});

const downloadUrl = computed(() => {
  return buildDownloadUrl(props.taxonId);
});

function getNonSpeciesNames(names) {
  const diffNames = names.filter((name) => name !== taxon.value.name);
  return diffNames.length > 0 ? diffNames.join(', ') : 'none';
}
</script>

<style scoped></style>
