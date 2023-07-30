<template>
    <div class="home-page">
        <SideBar @getExpInfo="getExpInfo" />
        <div class="right-banner">
            <div class="box-card">
                <el-card class="inner-card">
                    <div>
                        <div class="title">{{ expName }}</div>
                        <div class="desc">
                            Experiment ID: 0 Artifact Location:
                            file:///D:/Code/Web/MLFLow/mlruns/0
                        </div>
                    </div>
                </el-card>
                <el-card class="inner-card">
                    <div>
                        <div class="title">实验描述</div>
                        <div class="desc">{{ expDesc }}</div>
                    </div>
                </el-card>
            </div>
            <el-divider />
            <el-row class="refresh-row" :gutter="10">
                <el-col :span="2">
                    <el-button type="primary" @click="refreshData">
                        <el-icon class="el-icon--right">
                            <Refresh class="refresh" /> </el-icon
                        >刷新
                    </el-button>
                </el-col>
                <el-col :span="2">
                    <el-button type="success" @click="handleAna">
                        <el-icon> <View /> </el-icon>查看分析
                    </el-button>
                </el-col>
                <el-col :span="11"></el-col>
                <el-col :span="4">
                    <el-select
                        v-model="exp_dataset.data_set"
                        clearable
                        placeholder="选择数据集"
                        @change="changeDataset"
                    >
                        <el-option
                            style="text-indent: 1em"
                            v-for="item in exp_dataset.data_set_options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-col>
                <el-col :span="5">
                    <el-select
                        v-model="exp_dataset.data_radio"
                        clearable
                        placeholder="选择标记数据划分比例"
                        @change="changeRatio"
                    >
                        <el-option
                            style="text-indent: 1em"
                            v-for="item in exp_dataset.data_ratio_options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </el-col>
            </el-row>
            <el-divider />
            <el-card>
                <el-table
                    :data="tableData"
                    style="width: 100%"
                    border
                    :default-sort="{ prop: 'created', order: 'descending' }"
                >
                    <el-table-column label="Name">
                        <template #default="scope">
                            <el-popover
                                effect="light"
                                trigger="hover"
                                placement="left"
                                width="auto"
                            >
                                <template #default>
                                    <div>name: {{ scope.row.name }}</div>
                                    <div>address: {{ scope.row.version }}</div>
                                </template>
                                <template #reference>
                                    <el-button
                                        link
                                        type="primary"
                                        @click="toDetail(scope.row)"
                                        >{{ scope.row.name }}</el-button
                                    >
                                </template>
                            </el-popover>
                        </template>
                    </el-table-column>
                    <el-table-column label="Created" sortable>
                        <template #default="scope">
                            <div style="display: flex; align-items: center">
                                <el-icon>
                                    <CircleCheck style="color: green" />
                                </el-icon>
                                <span style="margin-left: 10px">{{
                                    scope.row.created
                                }}</span>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="Duration" sortable>
                        <template #default="scope">
                            <div style="display: flex; align-items: center">
                                <el-icon>
                                    <timer />
                                </el-icon>
                                <span style="margin-left: 10px">{{
                                    scope.row.duration
                                }}</span>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="Source">
                        <template #default="scope">
                            <div style="display: flex; align-items: center">
                                <el-icon>
                                    <Platform style="color: rgb(93 148 235)" />
                                </el-icon>
                                <span style="margin-left: 10px">{{
                                    scope.row.source
                                }}</span>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="Version">
                        <template #default="scope">
                            <div style="display: flex; align-items: center">
                                <el-tag>{{ scope.row.version }}</el-tag>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="Models">
                        <template #default="scope">
                            <div style="display: flex; align-items: center">
                                <el-icon>
                                    <Grid color="rgb(103, 210, 102)" />
                                </el-icon>
                                <span style="margin-left: 10px">{{
                                    scope.row.models
                                }}</span>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="Operations" width="210">
                        <template #default="scope">
                            <el-button
                                size="small"
                                @click="handleEdit(scope.$index, scope.row)"
                            >
                                <el-icon> <Edit /> </el-icon>编辑
                            </el-button>
                            <el-button
                                size="small"
                                type="danger"
                                @click="handleDelete(scope.$index, scope.row)"
                            >
                                <el-icon> <Delete /> </el-icon>删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination
                    style="justify-content: center; margin-top: 10px"
                    background
                    layout="prev, pager, next"
                    :default-page-size="6"
                    :total="totalPage"
                    @current-change="handleCurrentChange"
                />
            </el-card>
        </div>
        <el-dialog
            v-model="dialogData.dialogEditVisible"
            title="Rename Experiment"
        >
            <span>New experiment name</span>
            <el-input v-model="dialogData.editMsg" class="m-2" placeholder="" />
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogData.dialogEditVisible = false"
                        >取消</el-button
                    >
                    <el-button type="primary" @click="confirmUpdate"
                        >保存</el-button
                    >
                </span>
            </template>
        </el-dialog>

        <el-dialog
            v-model="dialogData.dialogDeleteVisible"
            title="Delete Experiment"
        >
            <span>{{ dialogData.deleteMsg }}</span>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogData.dialogDeleteVisible = false"
                        >取消</el-button
                    >
                    <el-button type="danger" @click="confirmDelete"
                        >删除</el-button
                    >
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import {
    Refresh,
    Timer,
    CircleCheck,
    Platform,
    Edit,
    Delete,
    Grid,
    View
} from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import {
    deleteExpDetail,
    getExpDataset,
    getExpsList,
    updateExpDetail
} from '@/api/experiments'
import { ElMessage } from 'element-plus'

const router = useRouter()

let exp_dataset = reactive({
    data_set: 'abalone',
    data_radio: 0.005,
    data_set_options: [
        {
            label: 'abalone',
            value: 'abalone'
        }
    ],
    data_ratio_options: [
        {
            label: '0.005',
            value: '0.005'
        }
    ]
})

let totalPage = ref(0)

const curWrapperExpId = ref()
const expName = ref('')
const expDesc = ref('')
let dialogData = reactive({
    currentItem: {
        id: '',
        name: '',
        created: '',
        duration: '',
        source: '',
        version: '',
        models: ''
    },
    dialogDeleteVisible: false,
    deleteMsg: '',
    dialogEditVisible: false,
    editMsg: ''
})

let getExpsInfoList = async (options: {
    dataset: string
    data_ratio: number
    page: number
}) => {
    const { dataset, data_ratio, page } = options
    tableData.value = []
    let res = await getExpsList('/experiment_list', {
        master_exp_id: curWrapperExpId.value,
        data_set: dataset,
        data_ratio: data_ratio,
        cur_page: page
    })
    totalPage.value = res.data.msg.total
    res.data.msg.list.map((item: any) => {
        tableData.value.push({
            id: item.id,
            name: item.name,
            created: item.created,
            duration: item.duration,
            source: item.dataset,
            version: item.version,
            models: item.dataset
        })
    })
}

onMounted(() => {
    getExpDataset('/exp_dataset').then((res) => {
        exp_dataset.data_set_options = res.data.msg.dataset.map((item: any) => {
            return { lable: item, value: item }
        })
        exp_dataset.data_ratio_options = res.data.msg.ratio.map((item: any) => {
            return { lable: item, value: item }
        })
    })
})

let changeDataset = () => {
    getExpsInfoList({
        dataset: exp_dataset.data_set,
        data_ratio: exp_dataset.data_radio,
        page: 0
    })
}
let changeRatio = () => {
    getExpsInfoList({
        dataset: exp_dataset.data_set,
        data_ratio: exp_dataset.data_radio,
        page: 0
    })
}

interface ExpList {
    id: string
    name: string
    created: string
    duration: string
    source: string
    version: string
    models: string
}

let tableData = ref<Array<ExpList>>([])

let getExpInfo = async (target: any) => {
    curWrapperExpId.value = target.id
    expName.value = target.name
    expDesc.value = target.desc
    getExpsInfoList({
        dataset: exp_dataset.data_set,
        data_ratio: exp_dataset.data_radio,
        page: 0
    })
}

let handleCurrentChange = (cur_page: number) => {
    getExpsInfoList({
        dataset: exp_dataset.data_set,
        data_ratio: exp_dataset.data_radio,
        page: cur_page - 1
    })
}

const toDetail = (item: any) => {
    router.push({
        path: `expdetail/${item.id}`
    })
}

const handleEdit = async (index: number, row: ExpList) => {
    dialogData.editMsg = row.name
    dialogData.dialogEditVisible = true
    dialogData.currentItem = row
}
const handleDelete = (index: number, row: ExpList) => {
    dialogData.deleteMsg = `是否删除 ${row.name} 实验的数据`
    dialogData.dialogDeleteVisible = true
    dialogData.currentItem = row
}

let confirmDelete = async () => {
    let resp = await deleteExpDetail('/experiment_list/', {
        exp_id: dialogData.currentItem.id
    })
    if (resp.data.msg === 'ok') {
        ElMessage('删除成功')
    }
    tableData.value = tableData.value.filter(
        (item) => item.id !== dialogData.currentItem.id
    )
    dialogData.dialogEditVisible = false
    dialogData.dialogDeleteVisible = false
}

let confirmUpdate = async () => {
    let resp = await updateExpDetail('/experiment_list/', {
        exp_id: dialogData.currentItem.id,
        exp_name: dialogData.editMsg
    })
    if (resp.data.msg === 'ok') {
        ElMessage('修改成功')
    }
    tableData.value.filter(
        (item) => item.id === dialogData.currentItem.id
    )[0].name = dialogData.editMsg
    dialogData.dialogEditVisible = false
    dialogData.dialogEditVisible = false
}

let refreshData = () => {
    getExpsInfoList({
        dataset: exp_dataset.data_set,
        data_ratio: exp_dataset.data_radio,
        page: 0
    })
}

let handleAna = () => {
    router.push({
        path: `/metrics/${curWrapperExpId.value}`
        // query: {
        //     id: curWrapperExpId.value
        // }
    })
}
</script>

<style lang="scss" scoped>
.home-page {
    display: flex;
    width: 100%;
    height: 100%;

    .right-banner {
        overflow: auto;
        padding: 20px;
        flex: 1;

        .box-card {
            display: flex;
            justify-content: space-between;
            align-items: center;

            .inner-card {
                overflow: auto;
                width: 49%;
                max-height: 200px;
            }
        }

        .title {
            text-size-adjust: 100%;
            -webkit-tap-highlight-color: rgb(0 0 0 / 0%);

            --antd-wave-shadow-color: #1890ff;
            --scroll-bar: 0;

            box-sizing: border-box;
            overflow-wrap: break-word;
            margin-top: 12px;
            margin-bottom: 5px;
            font-size: 20px;
            line-height: 28px;
            font-weight: 600;
            color: rgb(31 39 45);
        }

        .desc {
            // text-indent: 1em;
            overflow-wrap: break-word;
            font-size: 14px;
            line-height: 20px;
            color: rgb(93 114 131);
        }

        .refresh-row {
            margin: 20px 0;
        }
    }
}

.refresh {
    transition: all 0.7s;
    transform: rotate(120deg);
}
</style>
