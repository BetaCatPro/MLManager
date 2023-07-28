<template>
    <div class="side-bar">
        <div class="title">Experiments</div>
        <div class="search">
            <el-input
                v-model="search"
                class="m-2"
                placeholder="搜索实验"
                :prefix-icon="Search"
                @change="handleChange"
            />
        </div>
        <div class="list">
            <ul>
                <li
                    class="li-box"
                    @click="handleClick(item)"
                    v-for="item in experiments_data"
                    :key="item.id"
                    :class="{ isactive: item.id == curItem }"
                >
                    <span>{{ item.name }}</span>
                    <IconEpEditPen
                        class="icon"
                        @click.prevent="handleEdit(item)"
                    />
                    <IconEpDelete
                        class="icon"
                        @click.prevent="handleDelete(item)"
                    />
                </li>
            </ul>
        </div>
    </div>

    <el-dialog v-model="dialogData.dialogEditVisible" title="Rename Experiment">
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
                <el-button type="danger" @click="confirmDelete">删除</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { getAllExps, updateExpName, deleteExpName } from '@/api/experiments'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { onBeforeMount, reactive, ref } from 'vue'

const emit = defineEmits(['getExpInfo'])

let experiments_data = ref<
    Array<{ id: string; name: string; desc: string; time: string }>
>([])

onBeforeMount(async () => {
    let res = await getAllExps('/experiments')
    res.data.map(
        (item: {
            pk: any
            fields: { name: any; description: any; time: any }
        }) => {
            experiments_data.value.push({
                id: item.pk,
                name: item.fields.name,
                desc: item.fields.description,
                time: item.fields.time
            })
        }
    )
    emit('getExpInfo', experiments_data.value[0])
})

let search = ref('')
let curItem = ref('1')

let dialogData = reactive({
    currentItem: { id: '0', name: '', desc: '', time: '' },
    dialogDeleteVisible: false,
    deleteMsg: '',
    dialogEditVisible: false,
    editMsg: ''
})

let handleChange = () => {
    console.log(search.value)
}

let handleClick = (item: {
    id: string
    name: string
    desc: string
    time: string
}) => {
    curItem.value = item.id
    emit('getExpInfo', item)
}

let handleEdit = (item: {
    id: string
    name: string
    desc: string
    time: string
}) => {
    dialogData.dialogEditVisible = true
    dialogData.editMsg = item.name
    dialogData.currentItem = item
}

let handleDelete = (item: {
    id: string
    name: string
    desc: string
    time: string
}) => {
    dialogData.dialogDeleteVisible = true
    dialogData.deleteMsg = `Experiment "${item.name}" (Experiment ID: ${item.id}) will be deleted.`
    dialogData.currentItem = item
}

let confirmDelete = async () => {
    let resp = await deleteExpName('/experiments', {
        master_exp_id: dialogData.currentItem.id
    })
    if (resp.data.msg === 'ok') {
        ElMessage('删除成功')
    }

    experiments_data.value = experiments_data.value.filter(
        (item) => item.id !== dialogData.currentItem.id
    )
    dialogData.dialogDeleteVisible = false
}

let confirmUpdate = async () => {
    let resp = await updateExpName('/experiments/', {
        master_exp_id: dialogData.currentItem.id,
        master_exp_name: dialogData.editMsg
    })
    if (resp.data.msg === 'ok') {
        ElMessage('修改成功')
    }
    experiments_data.value.filter(
        (item) => item.id === dialogData.currentItem.id
    )[0].name = dialogData.editMsg
    dialogData.dialogEditVisible = false
}
</script>

<style lang="scss" scoped>
.side-bar {
    display: flex;
    padding: 20px 20px 0;
    width: 25%;
    max-width: 320px;
    height: 100%;
    flex-direction: column;

    .title,
    .search,
    .list {
        margin-top: 20px;
        width: 100%;
    }

    .title {
        margin: 0;
        font-size: 22px;
        color: rgb(31 39 45);
        text-size-adjust: 100%;
        -webkit-tap-highlight-color: rgb(0 0 0 / 0%);
        box-sizing: border-box;
        overflow-wrap: break-word;
        line-height: 28px;
        font-weight: 600;

        --antd-wave-shadow-color: #1890ff;
        --scroll-bar: 0;
    }

    .list {
        padding: 0;
        color: #2374ca;

        .li-box {
            display: flex;
            align-items: center;
            padding-left: 5px;
            height: 35px;
            border-radius: 1px;
            border-left: 5px solid #fff;
            border-bottom: 1px dotted #dbe8f3;
            cursor: pointer;

            &:hover {
                background-color: #edf1f4;
            }

            span {
                flex: 1;
                margin-right: 3px;
            }

            .icon {
                cursor: pointer;
                margin-right: 10px;
            }
        }

        .isactive {
            background-color: #dbe8f3;
            border-left: 5px solid #2272b4;
        }
    }
}
</style>
