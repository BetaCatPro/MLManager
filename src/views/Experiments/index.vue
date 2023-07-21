<template>
    <div class="home-page">
        <IconEpFold />
    </div>
</template>

<script setup lang="ts">
import { getAllExps } from '@/api/experiments'

getAllExps('/experiments').then((res) => {
    console.log(res)
})
</script>
