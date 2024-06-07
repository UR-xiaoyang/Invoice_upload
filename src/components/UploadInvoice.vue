<!--上传发票-->
<script setup lang="ts">

</script>
<template>
  <div class="min-h-screen flex-1 flex flex-col items-center justify-center gap-8 bg-gray-950 text-white py-12 md:py-16 lg:py-20">
    <div class="text-center space-y-2">
      <h1 class="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-500 animate-text">
        Invoice upload server
      </h1>
      <p class="text-gray-400">Drag and drop your file or click to upload.</p>
    </div>
    <div class="w-full max-w-md border-2 border-gray-700 border-dashed rounded-md p-6 flex flex-col items-center justify-center space-y-4 cursor-pointer transition-colors hover:border-gray-500">
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
      <p class="text-gray-400">Drag and drop your file here</p>
      <input type="file" class="hidden" />
    </div>
    <div class="w-full max-w-md space-y-4 overflow-auto max-h-40 hide-scrollbar">
      <div class="bg-gray-800 rounded-md p-4 flex items-center gap-4">
        <div class="flex-1">
          <p class="font-medium">example.pdf</p>
          <p class="text-gray-400 text-sm">123 KB</p>
        </div>
        <button class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent h-10 w-10 text-gray-400 hover:text-gray-300">
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
      <div class="bg-gray-800 rounded-md p-4 flex items-center gap-4">

        <div class="flex-1">
          <p class="font-medium">invoice.pdf</p>
          <p class="text-gray-400 text-sm">256 KB</p>
        </div>
        <button class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent h-10 w-10 text-gray-400 hover:text-gray-300">
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
    </div>
  </div>
</template>

<style scoped>
.min-h-screen {
  min-height: 88.4vh;
}
</style>