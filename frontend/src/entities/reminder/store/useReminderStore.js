import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

const STORAGE_KEY = 'pregnancy_reminders'

export const useReminderStore = defineStore('reminders', () => {
  const reminders = ref([])

  const load = () => {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return
    try {
      reminders.value = JSON.parse(raw)
    } catch {
      reminders.value = []
      localStorage.removeItem(STORAGE_KEY)
    }
  }

  const persist = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(reminders.value))
  }

  const addReminder = (payload) => {
    reminders.value.unshift({
      id: `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      title: payload.title,
      date: payload.date,
      time: payload.time,
      done: false,
    })
    persist()
  }

  const toggleDone = (id) => {
    const item = reminders.value.find((it) => it.id === id)
    if (!item) return
    item.done = !item.done
    persist()
  }

  const clear = () => {
    reminders.value = []
    localStorage.removeItem(STORAGE_KEY)
  }

  const pendingCount = computed(() => reminders.value.filter((it) => !it.done).length)

  return {
    reminders,
    pendingCount,
    load,
    addReminder,
    toggleDone,
    clear,
  }
})
