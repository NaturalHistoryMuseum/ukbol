<template>
  <footer class="relative w-full bg-slate-200 px-4" aria-label="footer">
    <div class="flex flex-col h-full justify-center items-center gap-1">
      <div>
        An open source project by the Natural History Museum's Science Data
        Platforms team
      </div>
      <div class="flex gap-4 w-full justify-center">
        <div>
          Source code available on
          <a href="https://github.com/NaturalHistoryMuseum/ukbol">GitHub</a>
        </div>
        <div class="text-slate-400">|</div>
        <div>Contact: <a href="mailto:ukbol@nhm.ac.uk">ukbol@nhm.ac.uk</a></div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts"></script>

<style scoped>
footer {
  height: var(--foot-height);
}
</style>
