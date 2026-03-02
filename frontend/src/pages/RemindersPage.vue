<script setup>
import { reactive } from 'vue'
import dayjs from 'dayjs'
import { useReminderStore } from '../entities/reminder/store/useReminderStore'
import { createRemind } from '../shared/api/modules/remind'
const reminderStore = useReminderStore()

const form = reactive({
  title: '',
  date: dayjs().format('YYYY-MM-DD'),
  time: '09:00',
})

const submitReminder = () => {
  if (!form.title.trim()) {
    window.alert('请输入提醒标题')
    return
  }

  reminderStore.addReminder({
    title: form.title,
    date: form.date,
    time: form.time,
  })

  form.title = ''
}

// createRemind({
//   title: '产检',
//   date: '2024-06-20',
//   remind_time: '10:00',
// }).then(() => {
//   console.log('提醒创建成功')
// }).catch((err) => {
//   console.error('创建提醒失败', err)
// })
</script>

<template>
  <main class="safe-area-x px-4 pb-24 pt-6">
    <section class="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h1 class="text-xl font-bold text-slate-800">提醒中心</h1>

      <div class="mt-4 space-y-3">
        <label class="block">
          <span class="mb-1 block text-sm text-slate-600">提醒标题</span>
          <input
            v-model="form.title"
            type="text"
            class="h-11 w-full rounded-xl border border-slate-200 px-3 outline-none focus:border-pink-400"
            placeholder="例如：产检 / 补剂 / 喝水"
          />
        </label>

        <div class="grid grid-cols-2 gap-3">
          <label class="block">
            <span class="mb-1 block text-sm text-slate-600">日期</span>
            <input
              v-model="form.date"
              type="date"
              class="h-11 w-full rounded-xl border border-slate-200 px-3 outline-none focus:border-pink-400"
            />
          </label>
          <label class="block">
            <span class="mb-1 block text-sm text-slate-600">时间</span>
            <input
              v-model="form.time"
              type="time"
              class="h-11 w-full rounded-xl border border-slate-200 px-3 outline-none focus:border-pink-400"
            />
          </label>
        </div>
      </div>

      <button
        type="button"
        class="mt-4 h-11 w-full rounded-xl bg-pink-500 text-sm font-semibold text-white transition hover:bg-pink-600"
        @click="submitReminder"
      >
        添加提醒
      </button>
    </section>

    <section class="mt-4 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h2 class="text-base font-semibold text-slate-800">我的提醒</h2>
      <ul v-if="reminderStore.reminders.length" class="mt-3 space-y-2">
        <li v-for="item in reminderStore.reminders" :key="item.id" class="flex items-center gap-3 rounded-xl bg-slate-50 p-3">
          <input :checked="item.done" type="checkbox" class="h-4 w-4 accent-pink-500" @change="reminderStore.toggleDone(item.id)" />
          <div class="flex-1">
            <p :class="item.done ? 'text-slate-400 line-through' : 'text-slate-700'" class="text-sm font-medium">
              {{ item.title }}
            </p>
            <p class="text-xs text-slate-500">{{ item.date }} {{ item.time }}</p>
          </div>
        </li>
      </ul>
      <p v-else class="mt-3 text-sm text-slate-500">暂无提醒。</p>
    </section>
  </main>
</template>
