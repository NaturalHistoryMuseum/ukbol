<template>
  <div class="w-2/3 space-y-8 pt-10 pb-10">
    <section>
      <h1>About</h1>
      The UK Barcode of Life (UKBOL) project comprises a network of UK
      government agencies, biodiversity institutions and individual scientists
      engaged in DNA barcoding of the biota of the United Kingdom. There are
      approximately 75,000 eukaryote species in the UK and we aim to assemble
      and curate a comprehensive library of standardized DNA sequences (DNA
      barcodes) as a reference resource for research and management of this
      biodiversity. DNA barcoding provides a powerful tool for species
      identification from any type of tissue, any life stage, even from bulk
      samples or trace DNA left in the environment (eDNA). Reference DNA
      barcodes are linked to expertly identified voucher specimens in scientific
      collections with data deposited in a public, open-access database (<a
        href="http://www.boldsystems.org/"
        >BOLD</a
      >). Our effort is an integrated part of the International Barcode of Life
      Project (<a href="https://www.ibol.org/">iBOL</a>) and works closely with
      the Darwin Tree of Life project (<a
        href="https://www.darwintreeoflife.org/"
        >DToL</a
      >). To contribute to the project please contact us at:
      <a href="mailto:ukbol@nhm.ac.uk">ukbol@nhm.ac.uk</a>
    </section>

    <section>
      <h2>Background</h2>
      For background on the project read this report: Price, Briscoe, Misra and
      Broad (2020) DEFRA Centre of Excellence for DNA Methods: Evaluation of DNA
      barcode libraries used in the UK and developing an action plan to fill
      priority gaps. Natural England Joint Publication JR035 (<a
        href="https://publications.naturalengland.org.uk/publication/4670286621573120"
        >link</a
      >).
    </section>

    <section>
      <h2>Steering Group</h2>
      <ul class="list-disc pl-8">
        <li v-for="person in steeringGroup">
          <span class="font-bold">{{ person.name }}</span
          >, {{ person.inst }}
        </li>
      </ul>
    </section>

    <section>
      <h2>Objectives</h2>
      <ul class="list-disc pl-8">
        <li>Coordinate UK barcoding projects.</li>
        <li>Develop data standards.</li>
        <li>Develop field and lab SOPs.</li>
        <li>Develop an open access data portal.</li>
        <li>Develop and maintain a priority species list.</li>
        <li>Collect, identify and sequence priority species.</li>
        <li>Secure funding to sequence all UK species.</li>
      </ul>
    </section>

    <section>
      <h2>Funding</h2>
      The development of the UKBOL project has been supported by the Defra
      Centre of Excellence for DNA based methods. The Centre of Excellence aims
      to transform Defra group science by demonstrating the potential of
      existing methods, enabling the development of new methods, building
      capacity and providing a focal point for leadership in Defra, UK and
      across other government departments. Additional funding has been provided
      by Natural England, the Natural History Museum and in-kind support by all
      steering group members.
    </section>
  </div>
</template>

<script setup>
const steeringGroup = [
  { name: 'Ben Price', inst: 'Natural History Museum (coordinator)' },
  { name: 'Katie Clark', inst: 'Natural England' },
  { name: 'William Askew', inst: 'Natural England' },
  { name: 'Emma Keenan', inst: 'Natural Resources Wales' },
  { name: 'Iveta Matejusova', inst: 'Marine Scotland' },
  { name: 'Colin Bean', inst: 'NatureScot' },
  {
    name: 'David Bass',
    inst: 'Centre for Environment, Fisheries and Aquaculture Science (Cefas)',
  },
  { name: 'Paul Woodcock', inst: 'Joint Nature Conservation Committee' },
  { name: 'Peter Hollingsworth', inst: 'Royal Botanic Gardens Edinburgh' },
  { name: 'Helen James', inst: 'National Museum Northern Ireland' },
  { name: 'Ester Gaya', inst: 'Royal Botanic Gardens Kew' },
  { name: 'Vlad Blagoderov', inst: 'National Museums Scotland' },
  { name: 'Laura Jones', inst: 'National Botanic Garden of Wales' },
  { name: 'Mara Lawniczak', inst: 'Wellcome Sanger Institute' },
  { name: 'Craig Macadam', inst: 'Rethink Nature Partnership' },
  { name: 'David Roy', inst: 'Biological Records Centre, UKCEH' },
];
</script>

<style scoped></style>
