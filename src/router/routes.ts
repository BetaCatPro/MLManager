import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        component: () => import('@/components/layout/index.vue'),
        redirect: '/experiments',
        children: [
            {
                path: '/experiments',
                name: 'Experiments',
                component: () => import('@/views/Experiments/index.vue')
            },
            {
                path: '/expdetail/:id',
                name: 'ExperimentsDetails',
                component: () => import('@/views/ExperimentsDetails/index.vue')
            },
            {
                path: '/expdetail/:id/metrics',
                name: 'ExperimentsDetailsMetrics',
                component: () =>
                    import('@/views/ExperimentsDetailsMetrics/index.vue')
            },
            {
                path: '/models',
                name: 'Models',
                component: () => import('@/views/Models/index.vue')
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
