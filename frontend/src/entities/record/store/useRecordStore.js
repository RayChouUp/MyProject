import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

const STORAGE_KEY = 'pregnancy_records'

export const useRecordStore = defineStore('records', () => {
  const records = ref([])

  const load = () => {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return
    try {
      records.value = JSON.parse(raw)
    } catch {
      records.value = []
      localStorage.removeItem(STORAGE_KEY)
    }
  }

  const persist = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(records.value))
  }

  const addRecord = (payload) => {
    records.value.unshift({
      id: `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      type: payload.type,
      value: payload.value,
      note: payload.note || '',
      date: payload.date,
    })
    persist()
  }

  const clear = () => {
    records.value = []
    localStorage.removeItem(STORAGE_KEY)
  }

  const latestFive = computed(() => records.value.slice(0, 5))

  return {
    records,
    latestFive,
    load,
    addRecord,
    clear,
  }
})
