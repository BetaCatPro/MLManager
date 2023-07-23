<template>
    <div class="app-wrapper">
        <Header />
        <div class="main-container">
            <AppMain class="app-main" />
        </div>
    </div>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
.app-wrapper {
    width: 100%;
    height: 100%;

    .main-container {
        width: 100%;
        height: calc(100% - 61px);
    }
}
</style>
