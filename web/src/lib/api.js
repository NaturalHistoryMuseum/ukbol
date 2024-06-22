import axios from 'axios';

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
  const objectIds = keys.map((key) => gbifTaxon[key]).join(',');
  // search for the image URL using the GBIF IDs
  const resolveResponse = (
    await axios.get('https://api.phylopic.org/resolve/gbif.org/species', {
      params: { objectIDs: objectIds },
    })
  ).data;
  const relativeImageUrl = resolveResponse['_links']['primaryImage']['href'];
  const fullImageUrl = `https://api.phylopic.org/${relativeImageUrl}`;
  // get the image data
  const imageResponse = (await axios.get(fullImageUrl)).data;
  const thumbnailUrl = imageResponse['_links']['thumbnailFiles'][0]['href'];
  // return the thumbnail url and the full image url for credit linking
  return {
    url: thumbnailUrl,
    link: `https://phylopic.org/${relativeImageUrl}`,
  };
}
