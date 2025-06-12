<template>
  <div>
    <h1 class="">Connect Your Data</h1>
    <p class="font-italic mb-8">Import and estimate your data directly from an external invoicing system (e.g. Odoo)</p>
    <v-row>
      <v-col cols="4">
        <v-text-field
        label="API Endpoint"
        v-model="store.apiEndpoint"
        prepend-icon="mdi-link"></v-text-field>
      </v-col>
      <v-col cols="4">
        <DateFilter :defaultRange="dateRange"></DateFilter>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5">
        <ConfidenceSlider></ConfidenceSlider>
      </v-col>
    </v-row>
    <fetch-data-button :api="store.apiEndpoint"></fetch-data-button>
  </div>
  <div v-if="!store.loaded && !store.isLoading">
    <NoResults></NoResults>
  </div>
  <div>
    <failed-steps-table></failed-steps-table>
  </div>
</template>

<script setup>
import { useDashboardStore } from '@/stores/useDashboardStore'

const store = useDashboardStore()
const dateRange = ref([])

// set default range
if (!store.filters.dateRange) {
  dateRange.value = [ new Date(2024, 7, 2), new Date(2024, 7, 2) ] // month index is 1 off from actual month
}
else {
  console.log(store.filters.dateRange)
  dateRange.value = [ new Date(store.filters.dateRange[0]), new Date(store.filters.dateRange[1])]
}
</script>