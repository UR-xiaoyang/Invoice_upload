<!--导航栏-->
<template>
    <header id = "导航栏" class="bg-gray-950 text-white py-4 px-6 flex items-center justify-between">
        <div class="flex items-center gap-4 w-full">
      <a href="#">
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
          class="h-6 w-6"
        >
          <path d="m8 3 4 8 5-5 5 15H2L8 3z"></path>
        </svg>
        <span class="sr-only">Acme Inc</span>
      </a>
      <div class="relative md:hidden w-full">
        <button @click="toggleDropdown" class="inline-flex items-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-10 rounded-full w-full justify-start">
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
            class="h-6 w-6 mr-2"
          >
            <line x1="4" x2="20" y1="12" y2="12"></line>
            <line x1="4" x2="20" y1="6" y2="6"></line>
            <line x1="4" x2="20" y1="18" y2="18"></line>
          </svg>
          <span>Menu</span>
        </button>
        <DropdownMenu :isVisible="dropdownMenuVisible" />


      </div>
      <div class="hidden md:flex items-center gap-4 w-full justify-between">
        <div class="flex items-center gap-4">
          <a class="hover:text-gray-300" href="#">
            查看发票
          </a>
          <a class="hover:text-gray-300" href="#">
            上传文件
          </a>
        </div>
        <div class="flex items-center gap-4">
          <a class="hover:text-gray-300" href="#">
            注册
          </a>
          <a class="hover:text-gray-300" href="#">
            登录
          </a>
        </div>
      </div>
    </div>
    </header>

</template>

<script>
import { defineComponent, ref } from 'vue';
import DropdownMenu from './DropdownMenu.vue';

// 组件名和变量名保持英文，但在注释中使用中文描述
export default defineComponent({
  components: {
    DropdownMenu,
  },
  setup() {
    const dropdownMenuVisible = ref(false);
    function toggleDropdown() {
      dropdownMenuVisible.value = !dropdownMenuVisible.value;
    }
    return {
      dropdownMenuVisible,
      toggleDropdown,
    };
  },
});
</script>
