<template>
  <div
    class="relative bg-[url('/images/homebg.jpg')] w-full bg-cover flex items-center justify-center"
  >
    <div class="text-slate-100 text-center">
      <h1 class="text-7xl bold">UK Barcode of Life</h1>
      <h2 class="text-2xl pb-10 text-slate-900">
        DNA barcoding the biota of the United Kingdom to assemble and curate a
        comprehensive library of standardized DNA sequences
      </h2>
      <div class="flex justify-stretch text-lg">
        <router-link
          to="about"
          class="flex-1 text-right hover:text-slate-200 font-bold text-slate-50 p-2"
        >
          About
        </router-link>
        <span class="p-2 font-bold">|</span>
        <router-link
          to="data"
          class="flex-1 text-left hover:text-slate-200 font-bold text-slate-50 p-2"
        >
          Browse
        </router-link>
      </div>
    </div>
    <div class="absolute right-0 bottom-0 p-1 text-sm text-white">
      Photo by
      <a href="https://unsplash.com/@mangofantasy">Tim Johnson</a> on
      <a href="https://unsplash.com/photos/green-leaf-CHv5D04_GWk">Unsplash</a>
    </div>
  </div>
</template>

<script setup></script>

<style scoped></style>
