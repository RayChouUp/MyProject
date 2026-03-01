<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)
</script>

<template>
  <h2 class="mb-4 text-2xl font-semibold text-slate-900 dark:text-slate-100">{{ msg }}</h2>

  <div class="mb-6 rounded-xl bg-slate-100 p-4 dark:bg-slate-700/40">
    <button
      type="button"
      class="rounded-lg bg-indigo-600 px-4 py-2 font-medium text-white transition hover:bg-indigo-500"
      @click="count++"
    >
      count is {{ count }}
    </button>
    <p class="mt-3 text-sm text-slate-600 dark:text-slate-300">
      Edit
      <code class="rounded bg-slate-200 px-1 py-0.5 dark:bg-slate-700">components/HelloWorld.vue</code>
      to test HMR
    </p>
  </div>

  <p class="mb-2 text-slate-700 dark:text-slate-200">
    Check out
    <a
      href="https://vuejs.org/guide/quick-start.html#local"
      target="_blank"
      class="font-medium text-indigo-600 hover:underline dark:text-indigo-400"
      >create-vue</a
    >, the official Vue + Vite starter
  </p>
  <p class="mb-2 text-slate-700 dark:text-slate-200">
    Learn more about IDE Support for Vue in the
    <a
      href="https://vuejs.org/guide/scaling-up/tooling.html#ide-support"
      target="_blank"
      class="font-medium text-indigo-600 hover:underline dark:text-indigo-400"
      >Vue Docs Scaling up Guide</a
    >.
  </p>
  <p class="text-sm text-slate-500 dark:text-slate-400">Click on the Vite and Vue logos to learn more</p>
</template>
