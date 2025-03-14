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
              :value="binSummaries.length"
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
              v-if="binSummaries.length > 0"
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
        <BINSummaryTable :bin-summaries="binSummaries"></BINSummaryTable>
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
import BINSummaryTable from './BINSummaryTable.vue';

const props = defineProps(['taxonId']);
const status = ref('Loading...');
const taxon = ref(null);
const gbifTaxon = ref(null);
const phylopicData = ref(null);
const binSummaries = ref([]);
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
  binSummaries.value = await getTaxonBins(props.taxonId);
  specimenCount.value = binSummaries.value.reduce(
    (acc, binSummary) => acc + binSummary.count,
    0,
  );
  status.value = '';
});

const downloadUrl = computed(() => {
  return buildDownloadUrl(props.taxonId);
});
</script>

<style scoped></style>
