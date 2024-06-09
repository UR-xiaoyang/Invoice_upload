<script setup lang="ts">

</script>

<template>
  <div class="min-h-screen flex-1 flex flex-col items-center justify-center gap-8 bg-gray-950 text-white py-12 md:py-16 lg:py-20 relative overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-t from-gray-950 to-transparent animate-arrow-up"></div>
    <div class="text-center space-y-2 z-10">
      <h1 class="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-purple-500 animate-text">
        Sign In
      </h1>
      <p class="text-gray-400">Sign in to your account to access our services.</p>
    </div>
    <div class="w-full max-w-md space-y-4 z-10">
      <div class="space-y-2">
        <label
          class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="email"
        >
          Email
        </label>
        <input
          class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          id="email"
          placeholder="Enter your email"
          type="email"
        />
      </div>
      <div class="space-y-2">
        <label
          class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          for="password"
        >
          Password
        </label>
        <input
          class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          id="password"
          placeholder="Enter your password"
          type="password"
        />
      </div>

      <button class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-custom-black text-primary-foreground hover:bg-custom-black:hover h-10 px-4 py-2 w-full">
        Sign In
      </button>

      <div class="text-center text-gray-400 text-sm">
        Don't have an account?{" "}
        <a class="text-blue-500 hover:underline" href="#">
          Sign Up
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url(../assets/sgin.css);
</style>