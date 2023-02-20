<template>
    <div class="home-page">
        <el-button type="primary">Primary</el-button>
        <IconEpFold class="v-icon" />
        <icon-ep-fold class="v-icon" />
        <IconEpBaseball class="v-icon"></IconEpBaseball>
    </div>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss">
.v-icon {
    display: inline-block;
    width: 1em;
    height: 1em;
    font-size: 1em;
}

.v-icon > svg {
    width: 100%;
    height: 100%;
}
</style>
