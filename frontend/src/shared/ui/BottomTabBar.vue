<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const tabs = [
  { label: '首页', to: '/home', icon: '🏠' },
  { label: '孕周', to: '/timeline', icon: '🗓️' },
  { label: '记录', to: '/records', icon: '📝' },
  { label: '提醒', to: '/reminders', icon: '⏰' },
  { label: '我的', to: '/profile', icon: '👤' },
]
</script>

<template>
  <nav class="fixed inset-x-0 bottom-0 z-30 mx-auto flex h-16 w-full max-w-[430px] border-t border-pink-100 bg-white/95 px-2 backdrop-blur">
    <RouterLink
      v-for="tab in tabs"
      :key="tab.to"
      :to="tab.to"
      class="flex min-w-0 flex-1 flex-col items-center justify-center gap-0.5 rounded-xl text-xs font-medium transition"
      :class="route.path === tab.to ? 'bg-pink-50 text-pink-600' : 'text-slate-500 hover:text-slate-700'"
    >
      <span class="text-base">{{ tab.icon }}</span>
      <span>{{ tab.label }}</span>
    </RouterLink>
  </nav>
</template>
