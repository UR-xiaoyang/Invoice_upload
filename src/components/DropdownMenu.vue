<!--导航栏列表-->
<script setup lang="ts">
import { defineProps, ref, onMounted } from 'vue';
import Cookies from 'js-cookie';
import { useRouter } from 'vue-router';

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false,
  },
});

const isLoggedIn = ref(false);
const username = ref('');
const router = useRouter();

onMounted(() => {
  const token = Cookies.get('token');
  const savedLoginInfo = localStorage.getItem('loginInfo');

  if (token && savedLoginInfo) {
    const parsedInfo = JSON.parse(savedLoginInfo);
    if (parsedInfo) {
      username.value = parsedInfo.username;
      isLoggedIn.value = true;
    }
  } else if (token) {
    // 如果只有token存在，没有loginInfo，模拟请求获取用户名并存储
    api.get('/user/info', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (response.status === 200) {
          const userInfo = response.data;
          username.value = userInfo.username;
          isLoggedIn.value = true;
          localStorage.setItem('loginInfo', JSON.stringify({
            username: userInfo.username,
            isLoggedIn: true,
          }));
        }
      })
      .catch((error) => {
        console.error('获取用户信息失败', error);
      });
  }
});

const logout = () => {
  isLoggedIn.value = false;
  username.value = '';
  localStorage.removeItem('loginInfo');
  Cookies.remove('token');
  router.push('/sign_in');
};
</script>

<template>
  <div v-if="isVisible" class="absolute top-full left-0 z-10 mt-2 w-full rounded-md bg-gray-950 py-2 shadow-lg">
    <a class="block px-4 py-2 text-sm hover:bg-gray-800 w-full" href="#">
      查看发票
    </a>
    <a class="block px-4 py-2 text-sm hover:bg-gray-800 w-full" href="#">
      上传文件
    </a>
    <div v-if="!isLoggedIn">
      <router-link class="block px-4 py-2 text-sm hover:bg-gray-800 w-full" to="/sign_up">
        注册
      </router-link>
      <router-link class="block px-4 py-2 text-sm hover:bg-gray-800 w-full" to="/sign_in">
        登陆
      </router-link>
    </div>
    <div v-else>
      <span class="block px-4 py-2 text-sm hover:bg-gray-800 w-full">
        欢迎 {{ username }}
      </span>
      <button @click="logout" class="block px-4 py-2 text-sm hover:bg-gray-800 w-full text-left">
        登出
      </button>
    </div>
  </div>
</template>

<style scoped>
</style>
