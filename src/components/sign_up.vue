<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue';
import { api } from '@/API/API_connect';
import type { 用户注册表单 } from '@/API/sign_up';

const formData = ref<用户注册表单>({
  用户名: '',
  密码: '',
  确认密码: '', // 添加确认密码字段
  邮箱: '',
  银行卡号: '',
  开户行: '',
  真实姓名: '',
  部门名称: '',
});

// 验证密码是否一致
const isPasswordMatch = (): boolean => {
  console.log('密码:', formData.value.密码, '确认密码:', formData.value.确认密码);
  return formData.value.密码 === formData.value.确认密码;
};

// 验证密码复杂度（包含数字和英文，长度至少6位）
function isPasswordComplex(): boolean {
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;
  return passwordRegex.test(formData.value.密码);
}

// 验证邮箱格式
function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// 在注册前进行验证
async function handleRegister() {
  if (!isPasswordMatch()) {
    alert('密码和确认密码不一致！');
    return;
  }

  if (!isPasswordComplex()) {
    alert('密码必须包含数字和英文，且长度至少为6位！');
    return;
  }

  if (!isValidEmail(formData.value.邮箱)) {
    alert('邮箱格式不正确！');
    return;
  }

  try {
    const response = await api.post('/user/sign_up', formData.value);
    console.log('注册成功:', response.data);
    alert('注册成功！');
  } catch (error) {

    console.error('用户注册时发生错误:', error.message);
    alert('用户可能存在', error.message);
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
            v-model="formData.用户名"
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
            v-model="formData.邮箱"
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
            v-model="formData.密码"
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
            v-model="formData.确认密码"
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
            v-model="formData.银行卡号"
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
            v-model="formData.开户行"
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
            placeholder="真实姓名"
            v-model="formData.真实姓名"
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
            v-model="formData.部门名称"
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