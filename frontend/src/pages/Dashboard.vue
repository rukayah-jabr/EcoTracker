<template>
  <div>
    <h1>Data Dashboard</h1>
    <!-- <DateFilter :value="store.filters.dateRange" @change="onDateChange" /> -->
    <!-- <CategoryFilter :value="store.filters.category" @change="onCategoryChange" /> -->
  </div>
</template>

<script setup>
import { useDashboardStore } from '@/stores/useDashboardStore'
import { onMounted } from 'vue'

const store = useDashboardStore()

function onDateChange(newRange) {
  store.updateFilter('dateRange', newRange)
}

function onCategoryChange(newCategory) {
  store.updateFilter('category', newCategory)
}
</script>
