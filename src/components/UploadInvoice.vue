<script setup lang="ts">
import { ref, computed } from 'vue';
import { api } from '@/API/API_connect';
import Cookies from 'js-cookie';

// 文件上传列表
const formData = ref({
  文件上传: [] as File[],
});
const token = ref('');
const 文件上传列表 = computed(() => formData.value?.文件上传 ?? []);

// 点击上传
function handleFile(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    for (let i = 0; i < input.files.length; i++) {
      formData.value.文件上传.push(input.files[i]);
    }
  }
}

// 拖拽上传
function handleDrop(event: DragEvent) {
  event.preventDefault();
  const files = event.dataTransfer?.files;
  if (files) {
    for (let i = 0; i < files.length; i++) {
      formData.value.文件上传.push(files[i]);
    }
  }
}

// 删除文件
function handleDelete(index: number) {
  formData.value.文件上传.splice(index, 1);
}

// 提交API
const upload_invoice = async () => {
  try {
    // 构建请求体
    const 传输表单 = new FormData();

    // 将所有文件添加到formData中
    formData.value.文件上传.forEach((file) => {
      传输表单.append('upload_file', file);
    });

    // 获取token
    const token = Cookies.get('token') ?? '';

    // 添加token
    const config = {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    };

    // 发起POST请求
    const 请求 = await api.post('/user/upload_invoice', 传输表单, config);

    // 检测响应
    if (请求.status === 200) {
      console.log("上传成功");
      // 清空文件上传列表
      formData.value.文件上传 = [];
      // 显示浏览器弹窗
      alert('上传成功');
    } else {
      console.log("上传失败", 请求.data);
    }
  } catch (error) {
    console.log("上传失败", error);
  }
}
</script>

<template>
  <div class="min-h-screen flex-1 flex flex-col items-center justify-center gap-8 bg-gray-950 text-white py-12 md:py-16 lg:py-20">
    <div class="text-center space-y-2">
      <h1 class="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-500 animate-text">
        发票上传服务器
      </h1>
      <p class="text-gray-400">让我们来上传你的发票吧～</p>
    </div>
    <div @dragover.prevent
         @drop.prevent="handleDrop"
         @click="$refs.fileInput.click()"
         class="w-full max-w-md border-2 border-gray-700 border-dashed rounded-md p-6 flex flex-col items-center justify-center space-y-4 cursor-pointer transition-colors hover:border-gray-500">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="h-12 w-12 text-gray-500"
      >
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="17 8 12 3 7 8"></polyline>
        <line x1="12" x2="12" y1="3" y2="15"></line>
      </svg>
      <p class="text-gray-400">拖拽或者点击选择文件</p>
      <input ref="fileInput"
             type="file"
             class="hidden"
             @change="handleFile" />
    </div>
    <!-- 文件列表展示 -->
    <div v-if="文件上传列表.length > 0" class="w-full max-w-md space-y-4 overflow-auto max-h-40 hide-scrollbar">
      <div v-for="(file, index) in 文件上传列表" :key="index" class="bg-gray-800 rounded-md p-4 flex items-center gap-4">
        <div class="flex-1">
          <p class="font-medium">{{ file.name }}</p>
          <p class="text-gray-400 text-sm">{{ (file.size / 1024).toFixed(2) }} KB</p>
        </div>
        <button @click="handleDelete(index)" class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent h-10 w-10 text-gray-400 hover:text-gray-300">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-5 w-5"
          >
            <path d="M18 6 6 18"></path>
            <path d="m6 6 12 12"></path>
          </svg>
        </button>
      </div>
      <button @click="upload_invoice" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-opacity-75">
        上传发票
      </button>
    </div>

    <div v-else class="w-full max-w-md border-2 border-gray-700 border-dashed rounded-md p-6 flex flex-col items-center justify-center space-y-4 cursor-pointer transition-colors hover:border-gray-500">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="h-5 w-5"
      >
        <path d="M18 6 6 18"></path>
        <path d="m6 6 12 12"></path>
      </svg>
      <p class="text-gray-400">暂无文件，拖拽或点击选择文件</p>
    </div>
  </div>
</template>

<style scoped>
.min-h-screen {
  min-height: 88.4vh;
}
</style>
