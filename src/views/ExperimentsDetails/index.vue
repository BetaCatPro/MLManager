<template>
    <div class="home-page">
        <div class="wrapper-card">
            <el-card class="box-card">
                <div>
                    <div class="name">{{ exp_data.exp_name }}</div>
                    <div class="info">
                        <span>Run ID: </span>{{ exp_data.run_id }}
                    </div>
                    <div class="info">
                        <span>Date: </span>
                        <el-icon>
                            <Timer style="color: rgb(205 58 112)" /> </el-icon
                        >{{ exp_data.date }}
                    </div>
                    <div class="info">
                        <span>Sources: </span>
                        <el-icon>
                            <Platform
                                style="color: rgb(93 148 235)"
                            /> </el-icon
                        >{{ exp_data.source }}
                    </div>
                    <div class="info">
                        <span>Duration: </span>{{ exp_data.duration }}
                    </div>
                    <div class="info">
                        <span>Status: </span>
                        <el-tag type="success">
                            {{ exp_data.status }}
                        </el-tag>
                    </div>
                </div>
            </el-card>
            <el-card class="box-card">
                <div>
                    <div class="name">Description</div>
                    <div class="info">{{ exp_data.desc }}</div>
                </div>
            </el-card>
            <el-card class="box-card">
                <div>
                    <div class="name">Tags</div>
                    <div class="info">
                        <el-tag v-for="tag in exp_data.tags" :key="tag">{{
                            tag
                        }}</el-tag>
                    </div>
                    <div class="name">Artifacts</div>
                    <div class="info">{{ exp_data.artifacts }}</div>
                </div>
            </el-card>
        </div>
        <el-divider />

        <div class="wrapper-card">
            <el-card class="box-card chart">
                <div class="name">Parameters</div>
                <el-table
                    :data="paramsData"
                    style="width: 100%"
                    border
                    :row-class-name="tableRowClassName"
                >
                    <el-table-column label="Name">
                        <template #default="scope">
                            <span style="margin-left: 10px">{{
                                scope.row.name
                            }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="Value">
                        <template #default="scope">
                            <div style="display: flex; align-items: center">
                                <el-tag style="margin-left: 10px">{{
                                    scope.row.value
                                }}</el-tag>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
            </el-card>
            <el-card class="box-card chart">
                <div>
                    <div class="name">Metrics</div>
                    <TDBarChart />
                </div>
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onBeforeMount, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useMlStateStore } from '@/stores/mlstore'
// import { storeToRefs } from 'pinia'
import { Platform, Timer } from '@element-plus/icons-vue'
import { getExpDetail } from '@/api/experiments'
import 'echarts-gl'

const route = useRoute()
const expId = route.params.id

let exp_data = reactive({
    data_set: '',
    exp_name: 'sedate-coch-124',
    run_id: '41235135b1kjb5k1jbkj123k1j4bk',
    date: '2012-12-12',
    source: 'mlflow',
    duration: '8.5s',
    status: 'FINISHED',
    desc: '实验使用 rednet 对比算法包括 coreg',
    parameters: {},
    metrics: {},
    tags: ['ssl', 'dnn'],
    artifacts: 'file://cscscs'
})

// const { exp_detail_data } = storeToRefs(useMlStateStore())
const { changeExpData } = useMlStateStore()

let paramsData = ref()
let metricsData = ref()
let defineMetrics = reactive<{ dataset: string; metrics: any }>({
    dataset: '',
    metrics: undefined
})

onBeforeMount(async () => {
    let resp = await getExpDetail('/experiment_detail', {
        exp_detail_id: expId
    })
    if (resp.status === 200) {
        let exp_detail = resp.data.msg.exp_detail
        let exp_detail_params = resp.data.msg.exp_params
        let exp_detail_metrics = resp.data.msg.exp_metrics

        exp_data.data_set = exp_detail.dataset
        exp_data.exp_name = exp_detail.name
        exp_data.run_id = exp_detail.runid
        exp_data.date = exp_detail.time
        exp_data.source = exp_detail.dataset
        exp_data.duration = exp_detail.duration
        exp_data.status = exp_detail.status
        exp_data.desc = exp_detail.description
        exp_data.tags = exp_detail.tags.split(',')

        paramsData.value = exp_detail_params
        metricsData.value = exp_detail_metrics
    }

    defineMetrics = {
        dataset: exp_data.data_set,
        metrics: metricsData.value
    }

    changeExpData(defineMetrics)
})

const tableRowClassName = ({ row, rowIndex }: { row: any; rowIndex: any }) => {
    console.log(row)
    if (rowIndex === 1) {
        return 'warning-row'
    } else if (rowIndex === 3) {
        return 'success-row'
    }
    return ''
}
</script>

<style lang="scss" scoped>
.el-table .warning-row {
    --el-table-tr-bg-color: var(--el-color-warning-light-9);
}

.el-table .success-row {
    --el-table-tr-bg-color: var(--el-color-success-light-9);
}

.wrapper-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    // flex-wrap: nowrap;

    .box-card {
        overflow: auto;
        margin: 10px;
        width: 100%;
        height: 220px;

        .name {
            // margin-bottom: 13px;
            font-size: 21px;
            color: rgb(31 39 45);
            text-size-adjust: 100%;
            -webkit-tap-highlight-color: rgb(0 0 0 / 0%);
            overflow-wrap: break-word;
            line-height: 28px;
            font-weight: 600;
            box-sizing: border-box;

            --antd-wave-shadow-color: #1890ff;
            --scroll-bar: 0;
        }

        .info {
            display: flex;
            align-items: center;
            margin-top: 6px;
            font-size: 15px;

            span {
                display: inline-block;
                margin-right: 8px;
                width: 80px;
                white-space: nowrap;
                color: rgb(93 114 131);
                text-size-adjust: 100%;
                -webkit-tap-highlight-color: rgb(0 0 0 / 0%);
                box-sizing: border-box;
                overflow-wrap: break-word;
                line-height: 16px;

                --antd-wave-shadow-color: #1890ff;
                --scroll-bar: 0;
            }
        }
    }

    .chart {
        height: 400px;
    }
}
</style>
