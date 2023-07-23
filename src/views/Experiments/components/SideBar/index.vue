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
                    v-for="item in testItems"
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
// import useRequest from '@/hooks/useRequest'
import { Search } from '@element-plus/icons-vue'
import { reactive, ref } from 'vue'

const emit = defineEmits(['getExpInfo'])

// const { data, loading, error, run } = useRequest({
//     url: 'https://hn.algolia.com/api/v1/search'
// })
// onMounted(() => {
//     run()
// })

let search = ref('')
let testItems = ref([
    {
        id: 1,
        name: 'Exp1'
    },
    {
        id: 2,
        name: 'Exp2'
    },
    {
        id: 3,
        name: 'Exp3'
    }
])
let curItem = ref(1)

let dialogData = reactive({
    currentItem: { id: 0, name: '' },
    dialogDeleteVisible: false,
    deleteMsg: '',
    dialogEditVisible: false,
    editMsg: ''
})

let handleChange = () => {
    console.log(search.value)
}

emit('getExpInfo', testItems.value[0])
let handleClick = (item: { id: number; name: string }) => {
    curItem.value = item.id
    emit('getExpInfo', item)
}

let handleEdit = (item: { id: number; name: string }) => {
    dialogData.dialogEditVisible = true
    dialogData.editMsg = item.name
    dialogData.currentItem = item
}

let handleDelete = (item: { id: number; name: string }) => {
    dialogData.dialogDeleteVisible = true
    dialogData.deleteMsg = `Experiment "${item.name}" (Experiment ID: ${item.id}) will be deleted.`
    dialogData.currentItem = item
}

let confirmDelete = () => {
    dialogData.dialogDeleteVisible = false
}

let confirmUpdate = () => {
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
