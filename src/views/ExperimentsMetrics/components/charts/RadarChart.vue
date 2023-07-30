<template>
    <div
        ref="chartRef"
        :class="props.className"
        :style="{ height: props.height, width: props.width }"
    />
</template>

<script lang="ts" setup>
import { ECharts, EChartOption, init } from 'echarts'
import { ref, onUnmounted, watch } from 'vue'
import 'echarts/theme/macarons'
import { useMlStateStore } from '@/stores/mlstore'
import { storeToRefs } from 'pinia'

const props = defineProps({
    className: {
        type: String,
        default: 'chart'
    },
    width: {
        type: String,
        default: '100%'
    },
    height: {
        type: String,
        default: '400px'
    },
    ratio: {
        type: Number,
        default: 0.005,
        require: true
    }
})

let chart: ECharts | undefined
const chartRef = ref<HTMLDivElement>()

// onMounted(() => {
//     initChart()
// })

const { exp_stat } = storeToRefs(useMlStateStore())

watch(exp_stat, (newVal, oldVal) => {
    let target = newVal.filter((item) => item.ratio === props.ratio)
    initChart(target)
    console.log(oldVal)
})

onUnmounted(() => {
    if (!chart) {
        return
    }
    chart.dispose()
    chart = undefined
})
let initChart = (data: any) => {
    chart = init(chartRef.value!, 'macarons')

    // let metrics =

    let co_data_value: any[] = []
    let m5p_data_value: any[] = []

    let indicators: { name: any; max: number }[] = []

    data.map((item: { [x: string]: any }) => {
        co_data_value.push(item['co_train_rmse'].toFixed(4))
        m5p_data_value.push(item['m5p_rmse'].toFixed(4))

        indicators.push({
            name: item.dataset,
            max: 0.3
        })
    })

    const option: EChartOption = {
        legend: {
            data: ['co_train_rmse', 'm5p_rmse']
        },
        radar: {
            // shape: 'circle',
            indicator: indicators
        },
        series: [
            {
                type: 'radar',
                data: [
                    {
                        value: co_data_value,
                        name: 'co-train-rmse',
                        label: {
                            show: true,
                            formatter: function (params: any) {
                                return params.value as string
                            }
                        }
                    },
                    {
                        value: m5p_data_value,
                        name: 'm5p-rmse',
                        symbol: 'rect',
                        symbolSize: 5,
                        lineStyle: {
                            type: 'dashed'
                        },
                        label: {
                            show: true,
                            formatter: function (params: any) {
                                return params.value as string
                            }
                        }
                    }
                ]
            }
        ]
    }
    chart.setOption(option)
}
</script>
