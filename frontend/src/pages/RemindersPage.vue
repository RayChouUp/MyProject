<script setup>
import { reactive, ref } from 'vue'
import dayjs from 'dayjs'
import { useReminderStore } from '../entities/reminder/store/useReminderStore'
import { createRemind, getReminds } from '../shared/api/modules/remind'
import { showLoadingToast, closeToast, showToast } from 'vant'
import { awaitWrapper } from '@/utils'
const reminderStore = useReminderStore()

const form = reactive({
  title: '',
  date: dayjs().format('YYYY-MM-DD'),
  remind_time: dayjs().format('HH:mm'),
})
const submitReminder = async () => {
  if (!form.title.trim()) {
    window.alert('请输入提醒标题')
    return
  }
  showLoadingToast({
    message: '创建中',
  })
  const [err, res] = await awaitWrapper(
    createRemind({
      title: form.title,
      date: form.date,
      remind_time: form.remind_time,
    })
  )
  closeToast()
  if (err) {
    showToast({
      message: err.message || '创建失败',
    })
    return
  }
  form.title = ''
  getReminderList()
}


const reminderList = ref([])
const getReminderList = () => {
  getReminds(20).then((data) => {
    reminderList.value = data
  }).catch((err) => {
  })
}

getReminderList()
const datePickerVisible = ref(false)
const toggleDatePicker = (visible) => {
  datePickerVisible.value = visible
}

const onConfirmDate = (date) => {
  form.date = dayjs(date).format('YYYY-MM-DD')
  toggleDatePicker(false)
}

const timePickerVisible = ref(false)
const toggleTimePicker = (visible) => {
  timePickerVisible.value = visible
}

const onConfirmTime = (time) => {
  console.log(time)
  form.remind_time = dayjs(time).format('HH:mm')
  toggleTimePicker(false)
}

const currentDate = ref(['2024', '01', '01'])
const currentTime = ref(['10', '00'])
</script>

<template>
  <main class="safe-area-x px-4 pb-24 pt-6">
    <section class="rounded-2xl  py-4 shadow-sm ring-1 ring-slate-100">
      <h1 class="text-xl font-bold text-slate-800 px-4 mb-2">提醒中心</h1>
      <van-cell-group>
        <van-field v-model="form.title" label="提醒标题" placeholder="请输入提醒标题" />
        <van-field v-model="form.date" label="日期" placeholder="请选择日期" @click="toggleDatePicker(true)" />
        <van-field v-model="form.remind_time" label="时间" placeholder="请选择时间" @click="toggleTimePicker(true)" />

      </van-cell-group>

      <div class="mt-4">
        <van-button type="primary" block @click="submitReminder">
          <span class="text-sm font-semibold ">添加提醒</span>
        </van-button>
      </div>
    </section>

    <section class="mt-4 rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
      <h2 class="text-base font-semibold text-slate-800">我的提醒</h2>
      <ul v-if="reminderList.length" class="mt-3 space-y-2">
        <li v-for="item in reminderList" :key="item.id" class="flex items-center gap-3 rounded-xl bg-slate-50 p-3">
          <input :checked="item.done" type="checkbox" class="h-4 w-4 accent-pink-500"
            @change="reminderStore.toggleDone(item.id)" />
          <div class="flex-1">
            <p :class="item.done ? 'text-slate-400 line-through' : 'text-slate-700'" class="text-sm font-medium">
              {{ item.title }}
            </p>
            <p class="text-xs text-slate-500">{{ item.date }} {{ item.remind_time }}</p>
          </div>
        </li>
      </ul>
      <p v-else class="mt-3 text-sm text-slate-500">暂无提醒。</p>
    </section>
    <van-popup v-model:show="datePickerVisible" position="bottom">
      <van-date-picker v-model="currentDate" title="选择日期" @confirm="onConfirmDate" />
    </van-popup>
    <van-popup v-model:show="timePickerVisible" position="bottom">
      <van-time-picker v-model="currentTime" title="选择时间" @confirm="onConfirmTime" />
    </van-popup>
  </main>
</template>
