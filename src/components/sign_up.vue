<script setup lang="ts">
import { ref } from 'vue';
import { api } from '@/API/API_connect'; // 调整路径以匹配你的实际目录结构
import type { 用户注册表单 } from '@/API/sign_up'; // 引入类型定义，路径根据实际情况调整

// 定义响应式表单数据
const formData = ref<用户注册表单>({
  用户名: '',
  密码: '',
  邮箱: '',
  银行卡号: '',
  开户行: '',
  真实姓名: '',
  部门名称: '',
});

// 处理注册逻辑
async function handleRegister() {
  try {
    // 发起POST请求进行用户注册
    const response = await api.post('/user/sign_up', formData.value); // 假设API_CONNECT已经设置了baseURL
    console.log('注册成功:', response.data);
    // 这里可以添加成功提示或页面跳转逻辑
  } catch (error) {
    // 记录错误信息
    console.error('用户注册时发生错误:', error.message);

    // 根据错误响应细化处理逻辑
    if (error.response && error.response.status === 400) {
      console.error('提交的注册信息有误');
      // 可以在此处显示错误提示给用户
    }
  }
}
</script>



<template>
  <div class="min-h-screen flex-1 flex flex-col items-center justify-center gap-8 bg-gray-950 text-white py-12 md:py-16 lg:py-20 relative overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-t from-gray-950 to-transparent animate-arrow-up"></div>
    <div class="text-center space-y-2 z-10">
      <h1 class="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-500 animate-text">
        注册
      </h1>
      <p class="text-gray-400">让我们创建一个账号</p>
    </div>
    <div class="w-full max-w-md space-y-4 z-10">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="space-y-2">
          <label
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="username"
          >
            用户名
          </label>
          <input
            class="color-changing-input flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 color-changing-input"
            id="username"
            placeholder="您想注册的用户名"
          />
        </div>
        <div class="space-y-2">
          <label
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="email"
          >
            邮箱
          </label>
          <input
            class="color-changing-input flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            id="email"
            placeholder="输入您的邮箱"
            type="email"
          />
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
            placeholder="输入您的密码"
            type="password"
          />
        </div>
        <div class="space-y-2">
          <label
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="confirm-password"
          >
            确认您的密码
          </label>
          <input
            class="color-changing-input flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            id="confirm-password"
            placeholder="再次输入您的密码"
            type="password"
          />
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="space-y-2">
          <label
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="bank-card-id"
          >
            银行卡号
          </label>
          <input
            class="color-changing-input flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            id="bank-card-id"
            placeholder="卡号请不要空格"
          />
        </div>
        <div class="space-y-2">
          <label
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="bank-name"
          >
            开户行
          </label>
          <input
            class="color-changing-input flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            id="bank-name"
            placeholder="请输入您的具体"
          />
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="space-y-2">
          <label
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="real-name"
          >
            真实姓名
          </label>
          <input
            class="color-changing-input flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            id="real-name"
            placeholder="报销部门"
          />
        </div>
        <div class="space-y-2">
          <label
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            for="department"
          >
            公司名称
          </label>
          <input
            class="color-changing-input flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            id="department"
            placeholder="报销单抬头"
          />
        </div>
      </div>
      <div class="col-span-2">

        <button @click="handleRegister" class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-custom-black text-primary-foreground hover:bg-custom-black:hover h-10 px-4 py-2 w-full">
          注册
        </button>

      </div>
      <div class="text-center text-gray-400 text-sm">
        你已经有账号了？
        <router-link class="text-blue-500 hover:underline" to="/sign_in">
          登陆
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