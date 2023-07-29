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
import { useMlStateStore } from '@/stores/mlstore'
import { storeToRefs } from 'pinia'
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
        default: '320px'
    }
})

const { exp_detail_data } = storeToRefs(useMlStateStore())
// const exp_detail_data = useMlStateStore().exp_detail_data as expInf
watch(exp_detail_data, (newVal) => {
    initChart(newVal)
})

let chart: ECharts | undefined
const chartRef = ref<HTMLDivElement>()

// onMounted(() => {
//     initChart()
// })

onUnmounted(() => {
    if (!chart) {
        return
    }
    chart.dispose()
    chart = undefined
})
let initChart = (newVal: {
    dataset: string
    metrics: { name: string; value: string }[]
}) => {
    var dataset = [newVal.dataset, newVal.dataset]
    var metrics: any[] = []
    var data: any[][] = []
    newVal.metrics.map((item, index) => {
        metrics.push(item.name)
        data.push([index, index, item.value])
    })
    chart = init(chartRef.value!, 'macarons')
    const option: EChartsOption = {
        tooltip: {},
        visualMap: {
            max: 0.4,
            inRange: {
                color: [
                    '#313695',
                    '#4575b4',
                    '#74add1',
                    '#abd9e9',
                    '#e0f3f8',
                    '#ffffbf',
                    '#fee090',
                    '#fdae61',
                    '#f46d43',
                    '#d73027',
                    '#a50026'
                ]
            }
        },
        xAxis3D: {
            type: 'category',
            data: dataset
        },
        yAxis3D: {
            type: 'category',
            data: metrics
        },
        zAxis3D: {
            type: 'value'
        },
        grid3D: {
            boxWidth: 100,
            boxDepth: 80,
            viewControl: {
                // projection: 'orthographic'
            },
            light: {
                main: {
                    intensity: 1.2,
                    shadow: true
                },
                ambient: {
                    intensity: 0.3
                }
            }
        },
        series: [
            {
                type: 'bar3D',
                data: data.map(function (item) {
                    return {
                        value: [item[1], item[0], item[2]]
                    }
                }),
                shading: 'lambert',
                label: {
                    fontSize: 13,
                    borderWidth: 1
                },
                emphasis: {
                    label: {
                        fontSize: 20,
                        color: '#900'
                    },
                    itemStyle: {
                        color: '#900'
                    }
                }
            }
        ]
    }
    chart.setOption(option)
}
</script>
