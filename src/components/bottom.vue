<!--底部信息-->
<template>
  <footer class="bg-gray-950 text-gray-400 py-4 px-6 flex items-center justify-between">
    <div>
      <a class="hover:text-gray-300" href="https://github.com/UR-xiaoyang/Invoice_upload">
项目仓库
        <i class="iconfont icon-github ml-1"></i>
      </a>
    </div>
    <div class="flex items-center">
      <span>时间：{{ currentTime }}</span>
      <span class="mx-2">|</span>
      <span>你的IP地址: {{ ip }}</span>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, onMounted} from 'vue';

// 获取当前时间
const currentTime = ref(new Date().toLocaleString());

// 定义定时器
onMounted(() => {
  setInterval(() => {
    currentTime.value = new Date().toLocaleString();
  }, 1000);
});

// IP获取
const ip = ref('');
import axios from 'axios';
axios.get('https://api.ipify.org?format=json')
  .then(response => {
    ip.value = response.data.ip;
  })
  .catch(error => {
    console.log(error);
  });

</script>

<style scoped>

</style>