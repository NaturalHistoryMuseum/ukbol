<template>
  <nav
    class="relative w-screen top-0 left-0"
    role="navigation"
    aria-label="main navigation"
  >
    <div class="flex space-x-10 items-center">
      <a class="" href="/">
        <img
          class=""
          src="/images/logos/logo-ukbol.png"
          alt="UK Barcode of Life | Home"
        />
      </a>
      <a v-for="[link, name] in links" :href="link" class="text-lg">
        {{ name }}
      </a>
    </div>
  </nav>
</template>

<script setup lang="ts">
const links = [
  ['/about', 'About'],
  ['/dna-barcoding', 'DNA Barcoding'],
  ['/priority-species', 'Priority Species'],
  ['/related-projects', 'Related Projects'],
];
</script>

<style scoped></style>
