<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '@/API/API_connect'; // 确保api已配置了合适的超时时间
import Cookies from 'js-cookie';

const router = useRouter();
let isLoggedIn = ref(false);
const username = ref('');
const password = ref('');

// 使用localStorage来持久化登录信息
const storageKey = 'loginInfo';

onMounted(() => {
  // 页面加载时，检查localStorage中是否有登录信息
  const savedLoginInfo = localStorage.getItem(storageKey);
  if (savedLoginInfo) {
    const parsedInfo = JSON.parse(savedLoginInfo);
    isLoggedIn.value = parsedInfo.isLoggedIn;
    username.value = parsedInfo.username;
  }
});

async function handleLogin() {
  try {
    const loginData = {
      用户名: username.value,
      密码: password.value,
    };

    const response = await Promise.race([
      api.post('/user/sign_in', loginData),
      new Promise((_, reject) => setTimeout(() => reject(new Error('请求超时')), 10000)), // 10秒超时
    ]);

    if (response.status === 200) {
      console.log('登录成功:', response.data);
      Cookies.set('token', response.data.access_token, { expires: 0.5 / 24 });
      isLoggedIn.value = true;
      // 保存登录信息到localStorage
      localStorage.setItem(storageKey, JSON.stringify({
        isLoggedIn: true,
        username: response.data.username,
      }));
      
      window.location.href = '/';
    } else {
      throw new Error('登录失败');
    }
  } catch (error) {
    if (error.message === '请求超时') {
      console.error('请求超时，请检查网络或后端响应速度');
      alert('登录失败: 请求超时');
    } else {
      console.error('登录时发生错误:', error.message);
      alert('登录失败: ' + getErrorMessage(error));
    }
  }
}

function getErrorMessage(error: any) {
  return error.response?.data?.message || error.message || '未知错误';
}
</script>

<template>
  <div class="min-h-screen flex-1 flex flex-col items-center justify-center gap-8 bg-gray-950 text-white py-12 md:py-16 lg:py-20 relative overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-t from-gray-950 to-transparent animate-arrow-up"></div>
    <div class="text-center space-y-2 z-10">
      <h1 class="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-500 animate-text">
        登陆
      </h1>
      <p class="text-gray-400">让我们来登陆一下开始上传吧</p>
    </div>
    <div class="w-full max-w-md space-y-4 z-10">
      <div class="space-y-2">
        <label
          class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="username"
        >
          用户名
        </label>
        <input
          class="color-changing-input flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          id="username"
          placeholder="请输入用户名"
          type="text"
          v-model="username"
        />
      </div>
      <div class="space-y-2">
        <label
          class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="password"
        >
          密码
        </label>
        <input
          class="color-changing-input flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          id="password"
          placeholder="请输入你的密码"
          type="password"
          v-model="password"
        />
      </div>

      <button @click="handleLogin" class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-custom-black text-primary-foreground hover:bg-custom-black:hover h-10 px-4 py-2 w-full">
        登陆
      </button>

      <div class="text-center text-gray-400 text-sm">
        你还没有账号？
        <router-link to="/sign_up" class="text-blue-500 hover:underline">
          注册
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url(../assets/sgin.css);
.color-changing-input {
  color: black;
}
</style>