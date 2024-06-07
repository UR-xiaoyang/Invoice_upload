<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import navigation from './components/navigation.vue'
import Upload_invoice from './components/UploadInvoice.vue'
import bottom from './components/bottom.vue'
</script>

<template>
  <div class="flex flex-col">
    <navigation />
    <Upload_invoice />
    <bottom />
  </div>
</template>

<style>
@import url(./assets/index.css);
</style>
