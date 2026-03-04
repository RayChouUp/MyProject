import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './app/router'
import setupVant from '@/plugins/vant'
const app = createApp(App)
setupVant(app)
app.use(createPinia())
app.use(router)

app.mount('#app')
