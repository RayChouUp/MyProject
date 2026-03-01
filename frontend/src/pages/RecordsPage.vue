<script setup>
import { reactive } from 'vue'
import dayjs from 'dayjs'
import { useRecordStore } from '../entities/record/store/useRecordStore'

const recordStore = useRecordStore()

const form = reactive({
  type: '体重',
  value: '',
  note: '',
  date: dayjs().format('YYYY-MM-DD'),
})

const submitRecord = () => {
  if (!form.value.trim()) {
    window.alert('请输入记录值')
    return
  }

  recordStore.addRecord({
    type: form.type,
    value: form.value,
    note: form.note,
    date: form.date,
  })

  form.value = ''
  form.note = ''
}
</script>

<template>
  <main class="safe-area-x px-4 pb-24 pt-6">
    <section class="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h1 class="text-xl font-bold text-slate-800">健康记录</h1>

      <div class="mt-4 space-y-3">
        <label class="block">
          <span class="mb-1 block text-sm text-slate-600">记录类型</span>
          <select v-model="form.type" class="h-11 w-full rounded-xl border border-slate-200 px-3 outline-none focus:border-pink-400">
            <option>体重</option>
            <option>血压</option>
            <option>胎动</option>
            <option>症状</option>
          </select>
        </label>

        <label class="block">
          <span class="mb-1 block text-sm text-slate-600">记录值</span>
          <input
            v-model="form.value"
            type="text"
            class="h-11 w-full rounded-xl border border-slate-200 px-3 outline-none focus:border-pink-400"
            placeholder="例如：56.2kg / 120-80 / 8次"
          />
        </label>

        <label class="block">
          <span class="mb-1 block text-sm text-slate-600">日期</span>
          <input
            v-model="form.date"
            type="date"
            class="h-11 w-full rounded-xl border border-slate-200 px-3 outline-none focus:border-pink-400"
          />
        </label>

        <label class="block">
          <span class="mb-1 block text-sm text-slate-600">备注（可选）</span>
          <textarea
            v-model="form.note"
            rows="3"
            class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-pink-400"
            placeholder="补充当日状态"
          />
        </label>
      </div>

      <button
        type="button"
        class="mt-4 h-11 w-full rounded-xl bg-pink-500 text-sm font-semibold text-white transition hover:bg-pink-600"
        @click="submitRecord"
      >
        保存记录
      </button>
    </section>

    <section class="mt-4 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h2 class="text-base font-semibold text-slate-800">记录列表</h2>
      <ul v-if="recordStore.records.length" class="mt-3 space-y-2">
        <li v-for="item in recordStore.records" :key="item.id" class="rounded-xl bg-slate-50 p-3">
          <div class="flex items-center justify-between">
            <p class="text-sm font-semibold text-slate-700">{{ item.type }} · {{ item.value }}</p>
            <span class="text-xs text-slate-500">{{ item.date }}</span>
          </div>
          <p v-if="item.note" class="mt-1 text-xs text-slate-500">{{ item.note }}</p>
        </li>
      </ul>
      <p v-else class="mt-3 text-sm text-slate-500">暂无记录。</p>
    </section>
  </main>
</template>
