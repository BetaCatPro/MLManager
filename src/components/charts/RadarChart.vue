<template>
    <div
        ref="chartRef"
        :class="props.className"
        :style="{ height: props.height, width: props.width }"
    />
</template>

<script lang="ts" setup>
import { ECharts, EChartsOption, init } from 'echarts'
import { ref, onMounted, onUnmounted } from 'vue'
import 'echarts/theme/macarons'

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
        default: '550px'
    }
})

let chart: ECharts | undefined
const chartRef = ref<HTMLDivElement>()

onMounted(() => {
    initChart()
})

onUnmounted(() => {
    if (!chart) {
        return
    }
    chart.dispose()
    chart = undefined
})
let initChart = () => {
    chart = init(chartRef.value!, 'macarons')
    const option: EChartsOption = {
        legend: {
            data: ['RMSE', 'MAE']
        },
        radar: {
            // shape: 'circle',
            indicator: [
                { name: 'Sales', max: 6500 },
                { name: 'Administration', max: 16000 },
                { name: 'Information Technology', max: 30000 },
                { name: 'Customer Support', max: 38000 },
                { name: 'Development', max: 52000 },
                { name: 'Marketing', max: 25000 },
                { name: 'Markeasting', max: 15000 },
                { name: 'Marketsing', max: 45000 },
                { name: 'Marsketing', max: 27000 },
                { name: 'Marsketing', max: 21000 },
                { name: 'Marketsing', max: 27000 },
                { name: 'Marsketing', max: 29000 },
                { name: 'Marsketing', max: 30000 },
                { name: 'Marketinsg', max: 31000 }
            ]
        },
        series: [
            {
                name: 'Budget vs spending',
                type: 'radar',
                data: [
                    {
                        value: [4200, 3000, 20000, 35000, 50000, 18000],
                        name: 'RMSE',
                        label: {
                            show: true,
                            formatter: function (params: any) {
                                return params.value as string
                            }
                        }
                    },
                    {
                        value: [5000, 14000, 28000, 26000, 42000, 21000],
                        name: 'MAE',
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
