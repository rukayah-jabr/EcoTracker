<template>
  <div>
    <h1 class="mb-5">Connect Your Data</h1>
    <v-text-field
    label="API Endpoint"
    v-model="store.apiEndpoint"
    prepend-icon="mdi-link"></v-text-field>
    <!-- <v-date-input
      v-model="dateRange"
      label="Select date range"
      max-width="368"
      multiple="range"
      class="mr-5"
      :oninput="onDateChange(dateRange)"
    ></v-date-input> -->
    <date-filter :defaultRange="dateRange"></date-filter>
    <fetch-data-button :api="store.apiEndpoint"></fetch-data-button>
  </div>
</template>

<script setup>
import { useDashboardStore } from '@/stores/useDashboardStore'
import { formatDateToYMD } from '@/utils/dateHelpers'

const store = useDashboardStore()

// set default range
const dateRange = ref([ new Date(2024, 7, 2), new Date(2024, 7, 2) ]) // month index is 1 off from actual month
</script>