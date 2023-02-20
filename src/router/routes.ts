import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        component: () => import('@/components/layout/MainLayout.vue'),
        children: [
            {
                path: '',
                name: 'Home',
                component: () => import('@/views/Home/index.vue')
            }
        ]
    }
]

routes.push({
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: () => import('@/views/NotFound/index.vue')
})

export default routes
