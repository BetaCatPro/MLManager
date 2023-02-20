import App from '@/App.vue'
import {createApp} from 'vue'
import ElementPlus from 'element-plus'
import { createPinia } from 'pinia'
import { createHead } from '@vueuse/head'
import generateRouter from './router'

// import mLibs from '@/libs'

const app = createApp(App)

const pinia = createPinia()
const head = createHead()
const router = generateRouter()

app.use(pinia)
app.use(head)
app.use(router)
app.use(ElementPlus)
// app.use(mLibs)

app.mount('#app')
