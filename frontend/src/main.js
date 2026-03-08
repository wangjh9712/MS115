import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

import App from './App.vue'
import router from './router'
import './styles/main.scss'
import { applyBeijingTimezone } from './utils/timezone'
import { initPerformanceMonitor } from './utils/performance'

const app = createApp(App)

applyBeijingTimezone()

// 初始化性能监控（开发环境）
initPerformanceMonitor()

app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })

app.mount('#app')
