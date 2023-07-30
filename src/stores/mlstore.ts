import { defineStore } from 'pinia'

interface expInf {
    dataset: string
    metrics: { name: string; value: string }[]
}

interface statInf {
    ratio: number
    dataset: string
    co_train_rmse: number
    m5p_rmse: number
}

export interface perInf {
    dataset: string
    res: {
        ratio: number
        result: { co_train_rmse: string; m5p_rmse: string }
    }[]
}

export const useMlStateStore = defineStore('ml', {
    state: () => ({
        exp_detail_data: {} as expInf,
        exp_stat: [] as statInf[],
        exp_per_stat: [] as perInf[]
    }),
    getters: {},
    actions: {
        changeExpData(payload: expInf) {
            this.exp_detail_data = payload
        },
        changeExpStatData(payload: statInf[]) {
            this.exp_stat = payload
        },
        changePerExpStatData(payload: perInf[]) {
            this.exp_per_stat = payload
        }
    }
})
