<template>
    <div
        ref="chartRef"
        :class="props.className"
        :style="{ height: props.height, width: props.width }"
    />
</template>

<script lang="ts" setup>
import { ECharts, EChartsOption, init } from 'echarts'
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
        default: '300px'
    },
    ratio: {
        type: Number,
        require: true,
        default: 0.005
    }
})

let chart: ECharts | undefined
const chartRef = ref<HTMLDivElement>()

const { exp_per_stat } = storeToRefs(useMlStateStore())

// onMounted(() => {
//     initChart()
// })

watch(exp_per_stat, (newVal, oldVal) => {
    initChart(newVal)
    console.log(oldVal)
})

onUnmounted(() => {
    if (!chart) {
        return
    }
    chart.dispose()
    chart = undefined
})
let initChart = (target: any) => {
    chart = init(chartRef.value!, 'macarons')

    let res = target.res.filter(
        (item: { ratio: number }) => item.ratio === props.ratio
    )[0].result

    let co_rmse = res.map((item: { co_train_rmse: string }) =>
        parseFloat(item.co_train_rmse).toFixed(3)
    )
    let m5p_rmse = res.map((item: { m5p_rmse: string }) =>
        parseFloat(item.m5p_rmse).toFixed(3)
    )

    const option: EChartsOption = {
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            orient: 'vertical',
            x: 'top',
            y: 'left'
        },
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                dataView: { readOnly: false },
                magicType: { type: ['line', 'bar'] },
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            name: '实验次数',
            nameRotate: '0',
            nameLocation: 'center',
            nameGap: 30,
            nameTextStyle: {
                padding: [0, 0, 0, 35]
            },
            type: 'category',
            boundaryGap: false,
            data: new Array(res.length).fill(0).map((item, index) => index + 1)
        },
        yAxis: {
            name: 'RMSE',
            nameRotate: '90',
            nameLocation: 'center',
            nameGap: 30,
            nameTextStyle: {
                padding: [0, 0, 0, 35]
            },
            type: 'value',
            axisLabel: {
                formatter: '{value}'
            }
        },
        series: [
            {
                name: '协同训练',
                type: 'line',
                data: co_rmse,
                markPoint: {
                    data: [
                        { type: 'max', name: 'Max' },
                        { type: 'min', name: 'Min' }
                    ]
                },
                markLine: {
                    data: [{ type: 'average', name: 'Avg' }]
                }
            },
            {
                name: 'M5P学习器',
                type: 'line',
                data: m5p_rmse,
                markLine: {
                    data: [
                        { type: 'average', name: 'Avg' },
                        [
                            {
                                symbol: 'none',
                                x: '90%',
                                yAxis: 'max'
                            },
                            {
                                symbol: 'circle',
                                label: {
                                    position: 'start',
                                    formatter: 'Max'
                                },
                                type: 'max',
                                name: '最高点'
                            }
                        ]
                    ]
                }
            }
        ]
    }
    chart.setOption(option)
}
</script>
