<template>
    <div class="header">
        <div class="logo" @click="refresh">
            <IconEpMoonNight class="icon" />
        </div>
        <div class="menu">
            <el-menu
                :default-active="activeIndex"
                class="el-menu-demo"
                mode="horizontal"
                background-color="#0b3574"
                text-color="#fff"
                active-text-color="#fff"
                @select="handleSelect"
            >
                <el-menu-item index="1">Experiments</el-menu-item>
                <!-- <el-menu-item index="2">Models</el-menu-item> -->
            </el-menu>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const activeIndex = ref('1')
const handleSelect = (key: string) => {
    let router_path = key === '1' ? 'experiments' : 'models'
    router.push({ path: `/${router_path}` })
}

const refresh = () => {
    router.push({ path: '/' })
}
</script>

<style lang="scss" scoped>
.header {
    display: flex;
    height: 61px;
    font-size: 13px;
    color: #e7f1fb;
    // box-sizing: border-box;
    background-color: #0b3574;
    text-size-adjust: 100%;
    -webkit-tap-highlight-color: rgb(0 0 0 / 0%);
    line-height: 1.5715;

    --antd-wave-shadow-color: #1890ff;
    --scroll-bar: 0;

    .logo {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-left: 15px;
        width: 60px;
        cursor: pointer;

        .icon {
            width: 70%;
            height: 70%;
            color: #ccdbe8;
        }
    }

    .menu {
        flex: 1;
    }

    ::v-deep .el-menu-item {
        margin-left: 30px;
    }

    ::v-deep .is-active {
        border-bottom: 5px solid rgb(67 201 237);
    }
}
</style>
