<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import { usePregnancyStore } from '../entities/pregnancy/store/usePregnancyStore'

const router = useRouter()
const pregnancyStore = usePregnancyStore()

const today = dayjs().format('YYYY-MM-DD')

const form = reactive({
  nickname: '',
  dueDate: '',
})

const startNow = () => {
  if (!form.nickname.trim() || !form.dueDate) {
    window.alert('请填写昵称和预产期')
    return
  }

  pregnancyStore.setupProfile({
    name: form.nickname,
    expectedDate: form.dueDate,
  })

  router.replace('/home')
}
</script>

<template>
  <main class="safe-area-x px-4 pb-8 pt-10">
    <section class="rounded-3xl bg-gradient-to-br from-pink-400 to-rose-500 p-6 text-white shadow-lg">
      <h1 class="text-2xl font-bold">欢迎来到孕期助手</h1>
      <p class="mt-2 text-sm text-pink-50">先完成初始化，建立你的专属孕期时间线与提醒系统。</p>
    </section>

    <section class="mt-6 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h2 class="text-base font-semibold text-slate-800">初始化信息</h2>

      <div class="mt-4 space-y-4">
        <label class="block">
          <span class="mb-1 block text-sm text-slate-600">昵称</span>
          <input
            v-model="form.nickname"
            type="text"
            class="h-11 w-full rounded-xl border border-slate-200 px-3 outline-none focus:border-pink-400"
            placeholder="例如：小暖"
          />
        </label>

        <label class="block">
          <span class="mb-1 block text-sm text-slate-600">预产期</span>
          <input
            v-model="form.dueDate"
            type="date"
            :min="today"
            class="h-11 w-full rounded-xl border border-slate-200 px-3 outline-none focus:border-pink-400"
          />
        </label>
      </div>

      <button
        type="button"
        class="mt-6 h-11 w-full rounded-xl bg-pink-500 text-sm font-semibold text-white transition hover:bg-pink-600"
        @click="startNow"
      >
        开始使用
      </button>
    </section>
  </main>
</template>
