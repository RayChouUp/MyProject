import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import dayjs from 'dayjs'

const STORAGE_KEY = 'pregnancy_profile'

export const usePregnancyStore = defineStore('pregnancy', () => {
  const nickname = ref('')
  const dueDate = ref('')
  const initialized = ref(false)

  const load = () => {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return
    try {
      const data = JSON.parse(raw)
      nickname.value = data.nickname || ''
      dueDate.value = data.dueDate || ''
      initialized.value = !!data.initialized
    } catch {
      localStorage.removeItem(STORAGE_KEY)
    }
  }

  const save = () => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        nickname: nickname.value,
        dueDate: dueDate.value,
        initialized: initialized.value,
      }),
    )
  }

  const setupProfile = ({ name, expectedDate }) => {
    nickname.value = name.trim()
    dueDate.value = expectedDate
    initialized.value = true
    localStorage.setItem('pregnancy_onboarding_done', '1')
    save()
  }

  const resetProfile = () => {
    nickname.value = ''
    dueDate.value = ''
    initialized.value = false
    localStorage.removeItem(STORAGE_KEY)
    localStorage.removeItem('pregnancy_onboarding_done')
  }

  const currentWeek = computed(() => {
    if (!dueDate.value) return 0
    const due = dayjs(dueDate.value)
    if (!due.isValid()) return 0

    const daysToDue = due.startOf('day').diff(dayjs().startOf('day'), 'day')
    const week = 40 - Math.floor(daysToDue / 7)
    return Math.max(1, Math.min(40, week))
  })

  const currentTrimester = computed(() => {
    const week = currentWeek.value
    if (week <= 13) return '孕早期'
    if (week <= 27) return '孕中期'
    return '孕晚期'
  })

  return {
    nickname,
    dueDate,
    initialized,
    currentWeek,
    currentTrimester,
    load,
    save,
    setupProfile,
    resetProfile,
  }
})
