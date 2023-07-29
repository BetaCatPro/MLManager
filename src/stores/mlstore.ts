import { defineStore } from 'pinia'

interface expInf {
    dataset: string
    metrics: { name: string; value: string }[]
}

export const useMlStateStore = defineStore('ml', {
    state: () => ({
        exp_detail_data: {} as expInf
    }),
    getters: {},
    actions: {
        changeExpData(payload: expInf) {
            this.exp_detail_data = payload
        }
    }
})
