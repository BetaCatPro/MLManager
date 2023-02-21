<template>
    <section class="app-main">
        <router-view v-slot="{ Component }" :key="key">
            <transition name="fade-transform" mode="out-in">
                <component :is="Component" />
            </transition>
        </router-view>
    </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {useRoute} from 'vue-router'
const route = useRoute()
const key = computed(()=> {
    return route.path
})
</script>

