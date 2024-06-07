<!--导航栏列表-->
<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <div v-if="isVisible" class="absolute top-full left-0 z-10 mt-2 w-full rounded-md bg-gray-950 py-2 shadow-lg">
    <a class="block px-4 py-2 text-sm hover:bg-gray-800 w-full" href="#">
      查看发票
    </a>
    <a class="block px-4 py-2 text-sm hover:bg-gray-800 w-full" href="#">
      上传文件
    </a>
    <a class="block px-4 py-2 text-sm hover:bg-gray-800 w-full" href="#">
      注册
    </a>
    <a class="block px-4 py-2 text-sm hover:bg-gray-800 w-full" href="#">
      登陆
    </a>
  </div>
</template>

<style scoped>

</style>