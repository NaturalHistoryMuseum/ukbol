<template>
  <nav
    class="relative h-full w-full bg-white px-4"
    role="navigation"
    aria-label="main navigation"
  >
    <div class="flex space-x-10 items-center">
      <RouterLink class="" to="/">
        <img
          class="p-2"
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
  ['data', 'Explore Data'],
  ['priority-species', 'Priority Species'],
  ['related-projects', 'Related Projects'],
];
</script>

<style scoped>
nav {
  height: var(--nav-height);
}
</style>
