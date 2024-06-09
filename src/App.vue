<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import navigation from './components/navigation.vue'
import bottom from './components/bottom.vue'
</script>

<template>
  <div id="app" class="flex flex-col">
    <navigation />
    <router-view />
    <bottom />
  </div>
</template>

<style>
@import url(./assets/index.css);
</style>
