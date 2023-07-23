<template>
    <div class="home-page">
        <SideBar @getExpInfo="getExpInfo" />
        <div class="right-banner">
            <el-card class="box-card">
                <div>
                    <div class="title">{{ expName }}</div>
                    <div class="desc">
                        Experiment ID: 0 Artifact Location:
                        file:///D:/Code/Web/MLFLow/mlruns/0
                    </div>
                </div>
                <div>
                    <div class="title">实验描述</div>
                    <div class="desc">外部算法比较的对比实验</div>
                </div>
            </el-card>
            <el-divider />
            <el-row class="refresh-row">
                <el-col :span="24">
                    <el-button type="primary">
                        <el-icon class="el-icon--right">
                            <Refresh class="refresh" /> </el-icon
                        >刷新
                    </el-button>
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
                                    <Platform
                                        style="color: rgb(93 148 235)"
                                    />
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
                    style=" justify-content: center;margin-top: 10px"
                    background
                    layout="prev, pager, next"
                    :default-page-size="6"
                    :total="20"
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
import { ref, reactive } from 'vue'
import {
    Refresh,
    Timer,
    CircleCheck,
    Platform,
    Edit,
    Delete,
    Grid
} from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface User {
    id: number
    name: string
    created: string
    duration: string
    source: string
    version: string
    models: string
}
const expName = ref('')
let dialogData = reactive({
    currentItem: { id: 0, name: '' },
    dialogDeleteVisible: false,
    deleteMsg: '',
    dialogEditVisible: false,
    editMsg: ''
})

let getExpInfo = (target: any) => {
    expName.value = target.name
}

const toDetail = (item: any) => {
    router.push({
        path: `expdetail/${item.id}`
    })
}

const handleEdit = (index: number, row: User) => {
    console.log(index, row)
    dialogData.editMsg = row.name
    dialogData.dialogEditVisible = true
}
const handleDelete = (index: number, row: User) => {
    console.log(index, row)
    dialogData.deleteMsg = `是否删除 ${row.name} 实验的数据`
    dialogData.dialogDeleteVisible = true
}

let confirmDelete = () => {
    dialogData.dialogDeleteVisible = false
}

let confirmUpdate = () => {
    dialogData.dialogEditVisible = false
}

const tableData: User[] = [
    {
        id: 0,
        name: 'Tom',
        created: '2016-05-03',
        duration: '8.5s',
        source: 'mlflows',
        version: 'v1.0',
        models: 'sklearn'
    },
    {
        id: 1,
        name: 'Tom',
        created: '2016-05-03',
        duration: '1.5s',
        source: 'mlflows',
        version: 'v1.0',
        models: 'sklearn'
    },
    {
        id: 0,
        name: 'Tom',
        created: '2018-05-03',
        duration: '4.5s',
        source: 'mlflows',
        version: 'v1.0',
        models: 'sklearn'
    },
    {
        id: 0,
        name: 'Tom',
        created: '2018-05-03',
        duration: '4.5s',
        source: 'mlflows',
        version: 'v1.0',
        models: 'sklearn'
    },
    {
        id: 0,
        name: 'Tom',
        created: '2018-05-03',
        duration: '4.5s',
        source: 'mlflows',
        version: 'v1.0',
        models: 'sklearn'
    },
    {
        id: 0,
        name: 'Tom',
        created: '2018-05-03',
        duration: '4.5s',
        source: 'mlflows',
        version: 'v1.0',
        models: 'sklearn'
    }
]
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
