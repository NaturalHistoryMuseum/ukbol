<template>
  <div class="bg-slate-100 flex flex-col h-full">
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
          <Badge label="UKSI TVK" :value="taxon.id" colour="cyan"></Badge>
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
      <div class="flex-none p-4 flex flex-col gap-4 items-end justify-between">
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
            class="border-2 text-white p-2 border-black bg-slate-500 rounded-md hover:text-slate-100"
            :href="downloadUrl"
          >
            Download as CSV
            <FontAwesomeIcon class="pl-2" :icon="faDownload"></FontAwesomeIcon>
          </a>
        </div>
      </div>
    </div>
    <div class="px-2 overflow-y-auto">
      <table class="w-full table-auto text-left text-sm">
        <thead class="sticky top-0 z-10">
          <tr>
            <th
              v-for="header in headers"
              class="border-b font-medium p-4 text-left bg-slate-400"
            >
              {{ header }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="binGroup in binGroups"
            :key="binGroup.bin"
            class="text-center bg-slate-200 even:bg-slate-300"
          >
            <td>
              <a
                target="_blank"
                :href="`https://www.boldsystems.org/index.php/Public_BarcodeCluster?clusteruri=${binGroup.bin}`"
              >
                {{ binGroup.bin }}
              </a>
            </td>
            <td>{{ binGroup.count }}</td>
            <td>{{ binGroup.ukCount }}</td>
            <td>{{ Array.from(binGroup.names).join(', ') }}</td>
            <td></td>
            <td></td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import Name from '../Name.vue';
import Badge from '../Badge.vue';
import { capitalise } from '../../lib/utils.js';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faDownload } from '@fortawesome/free-solid-svg-icons';
import {
  getGBIFData,
  getPhylopicData,
  getTaxon,
  getTaxonBins,
  buildDownloadUrl,
} from '../../lib/api.js';
import { computed } from 'vue';

const headers = [
  'BIN',
  '# specimens (all)',
  '# specimens (UK)',
  'Names in BIN',
  'Maximum distance within BIN',
  'Distance to Nearest Neighbour BIN',
  'Preferred BIN?',
];

const { taxonId } = defineProps(['taxonId']);

const taxon = await getTaxon(taxonId);
const gbifTaxon = await getGBIFData(taxon.name, taxon.rank);
const phylopicData = !gbifTaxon ? null : await getPhylopicData(gbifTaxon);
const binGroups = await getTaxonBins(taxonId);
const specimenCount = binGroups.reduce((acc, bin) => acc + bin.count, 0);

const downloadUrl = computed(() => {
  return buildDownloadUrl(taxonId);
});
</script>

<style scoped></style>
