import { defineStore } from 'pinia'

export const useMlStateStore = defineStore('ml', {
    state: () => ({
        ml_list: []
    }),
    getters: {},
    actions: {
        async addMl(ml: any[]) {
            this.ml_list.push(...ml)
        }
    }
})
