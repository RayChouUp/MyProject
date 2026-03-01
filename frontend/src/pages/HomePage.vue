<script setup>
import { computed } from 'vue'
import dayjs from 'dayjs'
import { usePregnancyStore } from '../entities/pregnancy/store/usePregnancyStore'
import { useRecordStore } from '../entities/record/store/useRecordStore'
import { useReminderStore } from '../entities/reminder/store/useReminderStore'

const pregnancyStore = usePregnancyStore()
const recordStore = useRecordStore()
const reminderStore = useReminderStore()

const tips = {
  孕早期: '补充叶酸、保持规律作息，避免重体力活动。',
  孕中期: '关注体重增长曲线，适量散步和拉伸。',
  孕晚期: '准备待产包，留意胎动与产检频率。',
}

const todayText = computed(() => dayjs().format('YYYY年MM月DD日'))
</script>

<template>
  <main class="safe-area-x px-4 pb-24 pt-6">
    <section class="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <p class="text-xs text-slate-500">{{ todayText }}</p>
      <h1 class="mt-2 text-xl font-bold text-slate-800">你好，{{ pregnancyStore.nickname || '准妈妈' }}</h1>
      <div class="mt-4 grid grid-cols-3 gap-3 text-center">
        <div class="rounded-xl bg-pink-50 p-3">
          <p class="text-xs text-pink-500">当前孕周</p>
          <p class="mt-1 text-lg font-bold text-pink-600">{{ pregnancyStore.currentWeek }} 周</p>
        </div>
        <div class="rounded-xl bg-rose-50 p-3">
          <p class="text-xs text-rose-500">孕期阶段</p>
          <p class="mt-1 text-lg font-bold text-rose-600">{{ pregnancyStore.currentTrimester }}</p>
        </div>
        <div class="rounded-xl bg-amber-50 p-3">
          <p class="text-xs text-amber-500">待办提醒</p>
          <p class="mt-1 text-lg font-bold text-amber-600">{{ reminderStore.pendingCount }}</p>
        </div>
      </div>
    </section>

    <section class="mt-4 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h2 class="text-base font-semibold text-slate-800">今日建议</h2>
      <p class="mt-2 text-sm leading-6 text-slate-600">{{ tips[pregnancyStore.currentTrimester] }}</p>
    </section>

    <section class="mt-4 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h2 class="text-base font-semibold text-slate-800">最近记录</h2>
      <ul v-if="recordStore.latestFive.length" class="mt-3 space-y-2">
        <li
          v-for="item in recordStore.latestFive"
          :key="item.id"
          class="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2 text-sm"
        >
          <div>
            <p class="font-medium text-slate-700">{{ item.type }}：{{ item.value }}</p>
            <p class="text-xs text-slate-500">{{ item.date }}</p>
          </div>
        </li>
      </ul>
      <p v-else class="mt-3 text-sm text-slate-500">还没有记录，去“记录”页添加第一条吧。</p>
    </section>
  </main>
</template>
