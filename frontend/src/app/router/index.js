import { createRouter, createWebHistory } from 'vue-router'

import OnboardingPage from '../../pages/OnboardingPage.vue'
import HomePage from '../../pages/HomePage.vue'
import TimelinePage from '../../pages/TimelinePage.vue'
import RecordsPage from '../../pages/RecordsPage.vue'
import RemindersPage from '../../pages/RemindersPage.vue'
import ProfilePage from '../../pages/ProfilePage.vue'

const routes = [
  {
    path: '/',
    redirect: () => (localStorage.getItem('pregnancy_onboarding_done') === '1' ? '/home' : '/onboarding'),
  },
  {
    path: '/onboarding',
    name: 'onboarding',
    component: OnboardingPage,
    meta: { showTabBar: false, title: '初始化' },
  },
  {
    path: '/home',
    name: 'home',
    component: HomePage,
    meta: { showTabBar: true, title: '首页' },
  },
  {
    path: '/timeline',
    name: 'timeline',
    component: TimelinePage,
    meta: { showTabBar: true, title: '孕周' },
  },
  {
    path: '/records',
    name: 'records',
    component: RecordsPage,
    meta: { showTabBar: true, title: '记录' },
  },
  {
    path: '/reminders',
    name: 'reminders',
    component: RemindersPage,
    meta: { showTabBar: true, title: '提醒' },
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage,
    meta: { showTabBar: true, title: '我的' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  // const done = localStorage.getItem('pregnancy_onboarding_done') === '1'
  // if (!done && to.path !== '/onboarding') {
  //   return '/onboarding'
  // }
  // if (done && to.path === '/onboarding') {
  //   return '/home'
  // }
  return true
})

export default router
