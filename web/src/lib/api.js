import axios from 'axios';

export async function getTaxon(taxonId) {
  return (await axios.get(`/api/taxon/${taxonId}`)).data;
}

export async function getRoots() {
  return (await axios.get('/api/taxon/roots')).data;
}

export async function getTaxonParents(taxonId) {
  return (await axios.get(`/api/taxon/${taxonId}/parents`)).data;
}

export async function getSuggestions(search, size) {
  return (
    await axios.get('/api/taxon/suggest', {
      params: {
        query: search,
        size: size,
      },
    })
  ).data;
}

export async function getTaxonBins(taxonId) {
  return (await axios.get(`/api/taxon/${taxonId}/bins`)).data;
}

export async function getGBIFData(name, rank) {
  const data = (
    await axios.get(
      `https://api.gbif.org/v1/species/match?name=${name}&rank=${rank}&strict=true`,
    )
  ).data;
  if (data.matchType === 'NONE') {
    return null;
  } else {
    return data;
  }
}

export async function getPhylopicData(gbifTaxon) {
  const keys = [
    'speciesKey',
    'genusKey',
    'familyKey',
    'orderKey',
    'classKey',
    'phylumKey',
    'kingdomKey',
  ];
  const objectIds = keys
    .filter((key) => Object.hasOwn(gbifTaxon, key))
    .map((key) => gbifTaxon[key])
    .join(',');
  // search for the image URL using the GBIF IDs
  const resolveResponse = (
    await axios.get('https://api.phylopic.org/resolve/gbif.org/species', {
      params: { objectIDs: objectIds },
    })
  ).data;
  const relativeImageUrl = resolveResponse['_links']['primaryImage']['href'];
  const fullImageUrl = `https://api.phylopic.org${relativeImageUrl}`;
  // get the image data
  const imageResponse = (await axios.get(fullImageUrl)).data;
  const svgUrl = imageResponse['_links']['vectorFile']['href'];
  // return the SVG url and the full image url for credit linking
  return {
    url: svgUrl,
    link: `https://phylopic.org${relativeImageUrl}`,
  };
}

export function buildDownloadUrl(taxonId) {
  return `/api/taxon/${taxonId}/download/specimens`;
}
