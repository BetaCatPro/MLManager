<template>
    <div class="home-page">
        <div class="wrapper-card">
            <el-card class="box-card" v-for="ratio in ratios" :key="ratio">
                <div class="inner-desc">
                    有标记数据划分标准:
                    <el-tag type="danger">{{ ratio }}</el-tag>
                </div>
                <RadarChart :ratio="ratio" />
            </el-card>
        </div>
        <el-divider />
        <el-row>
            <el-col :span="3"
                ><el-button type="default" style="margin-left: 10px"
                    >选择数据集</el-button
                ></el-col
            >
            <el-col :span="3"
                ><el-select
                    v-model="data_set"
                    clearable
                    placeholder="选择数据集"
                    @change="changeDataset"
                >
                    <el-option
                        style="text-indent: 1em"
                        v-for="item in data_set_options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    /> </el-select
            ></el-col>
        </el-row>
        <div class="wrapper-card">
            <el-card class="box-card" v-for="ratio in ratios" :key="ratio">
                <div class="inner-desc">
                    数据集: <el-tag>{{ data_set }}</el-tag> 有标记数据划分标准:
                    <el-tag type="danger">{{ ratio }}</el-tag>
                </div>
                <LineRaceChart :ratio="ratio" />
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import {
    getExpDataset,
    getExpStatistic,
    getPerExpStatistic
} from '@/api/experiments'
import { useMlStateStore } from '@/stores/mlstore'
import { onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const expId = route.params.id as string
const ratios = [0.005, 0.025, 0.05]

let data_set_options = ref()
let data_set = ref('abalone')

const { changeExpStatData, changePerExpStatData } = useMlStateStore()

onBeforeMount(() => {
    getExpDataset('/exp_dataset').then((res) => {
        data_set_options.value = res.data.msg.dataset.map((item: any) => {
            return { lable: item, value: item }
        })
    })

    getExpStatistic('/exp_statistic', { exp_id: expId }).then((res) => {
        changeExpStatData(res.data.msg)
    })

    getPerExpStatistic('/exp_per_statistic', {
        exp_id: expId,
        dataset: data_set.value
    }).then((res) => {
        changePerExpStatData(res.data.msg)
    })
})

let changeDataset = () => {
    getPerExpStatistic('/exp_per_statistic', {
        exp_id: expId,
        dataset: data_set.value
    }).then((res) => {
        changePerExpStatData(res.data.msg)
    })
}
</script>

<style lang="scss" scoped>
.home-page {
    // height: calc(100vh - 100px);

    .wrapper-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        height: 100%;
        padding: 10px;

        .box-card {
            overflow: auto;
            width: 33%;
            height: 70%;
            margin-bottom: 5px;

            .inner-desc {
                color: rgb(47, 41, 174);
                font-size: 19px;
                margin-bottom: 15px;
                text-align: center;
            }
        }
    }
}
</style>
