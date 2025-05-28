<template>
  <div>
    <h1 class="mb-5">Connect Your Data</h1>
    <v-text-field
    label="API Endpoint"
    v-model="store.apiEndpoint"
    prepend-icon="mdi-link"></v-text-field>
    <v-date-input
      v-model="store.filters.dateRange"
      label="Select date range"
      max-width="368"
      multiple="range"
      class="mr-5"
    ></v-date-input>
    <fetch-data-button :api="store.apiEndpoint"></fetch-data-button>
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