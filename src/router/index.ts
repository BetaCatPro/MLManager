import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'

export default () => {
    return createRouter({
        history: createWebHistory(),
        routes
    })
}
