<template>
    <div class="home-page">
        <el-card class="box-card">{{ id }}</el-card>
    </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const id = route.params.id
</script>
