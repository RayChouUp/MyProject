<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import BottomTabBar from './shared/ui/BottomTabBar.vue'
import { usePregnancyStore } from './entities/pregnancy/store/usePregnancyStore'
import { useRecordStore } from './entities/record/store/useRecordStore'
import { useReminderStore } from './entities/reminder/store/useReminderStore'

const route = useRoute()
const pregnancyStore = usePregnancyStore()
const recordStore = useRecordStore()
const reminderStore = useReminderStore()

const showTabBar = computed(() => !!route.meta.showTabBar)

onMounted(() => {
  pregnancyStore.load()
  recordStore.load()
  reminderStore.load()
})
</script>

<template>
  <div class="mx-auto min-h-screen w-full max-w-[430px] bg-slate-50 text-slate-800">
    <RouterView />
    <BottomTabBar v-if="showTabBar" />
  </div>
</template>
