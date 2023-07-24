<template>
    <div class="home-page">
        <div class="wrapper-card">
            <el-card class="box-card">
                <LineRaceChart />
            </el-card>
            <el-card class="box-card">
                <LineRaceChart />
            </el-card>
            <el-card class="box-card">
                <LineRaceChart />
            </el-card>
            <el-card class="box-card">
                <LineRaceChart />
            </el-card>
            <el-card class="box-card">
                <LineRaceChart />
            </el-card>
            <el-card class="box-card">
                <LineRaceChart />
            </el-card>
            <el-card class="box-card">
                <LineRaceChart />
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
.home-page {
    padding: 10px;
    height: calc(100vh - 100px);
}

.wrapper-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    height: 90%;

    .box-card {
        overflow: auto;
        margin: 10px;
        width: 48%;
        height: 56%;
    }
}
</style>
