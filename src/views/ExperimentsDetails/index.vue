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
                        <el-tag v-for="tag in exp_data.tags" :key="tag"
                            ><span>{{ tag }}</span></el-tag
                        >
                    </div>
                    <div class="name">Artifacts</div>
                    <div class="info">{{ exp_data.artifacts }}</div>
                </div>
            </el-card>
            <el-card class="box-card">
                <div>
                    <div class="name">Parameters</div>
                    <el-table :data="paramsData" style="width: 100%" border>
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
                                    <span style="margin-left: 10px">{{
                                        scope.row.value
                                    }}</span>
                                </div>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </el-card>
        </div>
        <el-divider />
        <div class="chart">
            <el-card class="box-card">
                <div>
                    <div class="name">Metrics</div>
                    <div class="wrapper-card">
                        <el-card class="box-card">
                            <RadarChart />
                        </el-card>
                        <el-card class="box-card">
                            <RadarChart />
                        </el-card>
                        <el-card class="box-card">
                            <RadarChart />
                        </el-card>
                    </div>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onBeforeMount, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { Platform, Timer } from '@element-plus/icons-vue'
import { getExpDetail } from '@/api/experiments'

const route = useRoute()
const expId = route.params.id

const exp_data = reactive({
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

const paramsData = [
    {
        id: 0,
        name: 'Tom',
        value: '2016-05-03'
    },
    {
        id: 0,
        name: 'L1',
        value: '2016-05-03'
    },
    {
        id: 0,
        name: 'Tom',
        value: '2016-05-03'
    }
]

onBeforeMount(async () => {
    let resp = await getExpDetail('/experiment_list', { exp_detail_id: expId })
    console.log(resp.data)
})
</script>

<style lang="scss" scoped>
.wrapper-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: nowrap;

    .box-card {
        overflow: auto;
        margin: 10px;
        width: 100%;
        height: 220px;

        .name {
            margin-bottom: 13px;
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
}

.chart {
    margin: 10px;
    height: 570px;

    .wrapper-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: nowrap;
        height: 100%;

        .box-card {
            overflow: auto;
            width: 100%;
            height: 100%;
        }
    }
}
</style>
