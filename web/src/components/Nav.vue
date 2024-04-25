<template>
  <nav
    class="relative w-screen top-0 left-0 bg-white px-4"
    role="navigation"
    aria-label="main navigation"
  >
    <div class="flex space-x-10 items-center">
      <RouterLink class="" to="/">
        <img
          class=""
          src="/images/logos/logo.png"
          alt="UK Barcode of Life | Home"
        />
      </RouterLink>
      <RouterLink
        v-for="[routeName, linkText] in links"
        :to="{ name: routeName }"
        class="text-lg"
        :class="{ 'font-bold': $route.name == routeName }"
      >
        {{ linkText }}
      </RouterLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
const links = [
  ['about', 'About'],
  ['dna-barcoding', 'DNA Barcoding'],
  ['priority-species', 'Priority Species'],
  ['related-projects', 'Related Projects'],
];
</script>

<style scoped></style>
