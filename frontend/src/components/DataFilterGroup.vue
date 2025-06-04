<template>
    <DateFilter :defaultRange=defaultRange></DateFilter>
    <!-- <CategoryFilter></CategoryFilter> -->
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useDashboardStore } from '../stores/useDashboardStore'

const store = useDashboardStore()
const defaultRange = [new Date(store.filters.dateRange[0]), new Date(store.filters.dateRange[1])]

</script>