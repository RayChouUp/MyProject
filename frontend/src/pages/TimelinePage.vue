<script setup>
import { computed } from 'vue'
import { usePregnancyStore } from '../entities/pregnancy/store/usePregnancyStore'

const pregnancyStore = usePregnancyStore()

const weekTips = [
  { from: 1, to: 13, title: '孕早期', desc: '重点是稳定情绪、补充叶酸、避免风险动作。' },
  { from: 14, to: 27, title: '孕中期', desc: '是相对舒适阶段，注意营养平衡与适量运动。' },
  { from: 28, to: 40, title: '孕晚期', desc: '准备分娩计划，按时产检，关注胎动变化。' },
]

const currentTip = computed(() => {
  return weekTips.find((item) => pregnancyStore.currentWeek >= item.from && pregnancyStore.currentWeek <= item.to)
})

const timeline = computed(() => {
  return Array.from({ length: 40 }, (_, i) => i + 1)
})
</script>

<template>
  <main class="safe-area-x px-4 pb-24 pt-6">
    <section class="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h1 class="text-xl font-bold text-slate-800">孕周时间线</h1>
      <p class="mt-2 text-sm text-slate-600">当前第 {{ pregnancyStore.currentWeek }} 周 · {{ currentTip?.title }}</p>
      <p class="mt-2 text-sm leading-6 text-slate-600">{{ currentTip?.desc }}</p>
    </section>

    <section class="mt-4 grid grid-cols-5 gap-2 rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-100">
      <div
        v-for="week in timeline"
        :key="week"
        class="flex h-10 items-center justify-center rounded-lg text-sm font-medium"
        :class="week === pregnancyStore.currentWeek ? 'bg-pink-500 text-white' : 'bg-slate-100 text-slate-600'"
      >
        W{{ week }}
      </div>
    </section>
  </main>
</template>
