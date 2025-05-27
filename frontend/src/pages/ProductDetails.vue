<template>
  <div>
    <h1>Product Details</h1>
  </div>
</template>

<script setup>
import { useDashboardStore } from '@/stores/useDashboardStore'

const store = useDashboardStore()

function onDateChange(newRange) {
  store.updateFilter('dateRange', newRange)
}

function onCategoryChange(newCategory) {
  store.updateFilter('category', newCategory)
}
</script>