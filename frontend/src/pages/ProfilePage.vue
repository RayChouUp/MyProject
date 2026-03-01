<script setup>
import { useRouter } from 'vue-router'
import { usePregnancyStore } from '../entities/pregnancy/store/usePregnancyStore'
import { useRecordStore } from '../entities/record/store/useRecordStore'
import { useReminderStore } from '../entities/reminder/store/useReminderStore'

const router = useRouter()
const pregnancyStore = usePregnancyStore()
const recordStore = useRecordStore()
const reminderStore = useReminderStore()

const resetAll = () => {
  const ok = window.confirm('将清空个人资料、记录和提醒，是否继续？')
  if (!ok) return

  pregnancyStore.resetProfile()
  recordStore.clear()
  reminderStore.clear()
  router.replace('/onboarding')
}
</script>

<template>
  <main class="safe-area-x px-4 pb-24 pt-6">
    <section class="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h1 class="text-xl font-bold text-slate-800">个人中心</h1>

      <dl class="mt-4 space-y-3 text-sm">
        <div class="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2">
          <dt class="text-slate-500">昵称</dt>
          <dd class="font-medium text-slate-700">{{ pregnancyStore.nickname || '-' }}</dd>
        </div>
        <div class="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2">
          <dt class="text-slate-500">预产期</dt>
          <dd class="font-medium text-slate-700">{{ pregnancyStore.dueDate || '-' }}</dd>
        </div>
        <div class="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2">
          <dt class="text-slate-500">记录条数</dt>
          <dd class="font-medium text-slate-700">{{ recordStore.records.length }}</dd>
        </div>
      </dl>

      <button
        type="button"
        class="mt-6 h-11 w-full rounded-xl bg-slate-800 text-sm font-semibold text-white transition hover:bg-slate-900"
        @click="resetAll"
      >
        重置并重新初始化
      </button>
    </section>
  </main>
</template>
