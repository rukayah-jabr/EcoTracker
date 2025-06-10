<template>
  <div>
      <BarChart v-if="store.loaded" title="Emissions Over Time" :series="series" :xaxis="categories"/>
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore'
import { computed } from 'vue'

const store = useDashboardStore()

// Group emissions data by date
const purchaseCo2 = computed(() => groupEmissionByDate("co2_purchase"))
const transportCo2 = computed(() => groupEmissionByDate("co2_transport"))
const totalCo2 = computed(() => groupEmissionByDate("co2_total"))

// Set x-axis (dates)
const categories = computed(() =>
  sortGroup(totalCo2.value).map(([date]) => date)
)

// Set stacked bar chart data
const purchaseData = computed(() =>
  sortGroup(purchaseCo2.value).map(([, val]) => Number(val.toFixed(2)))
)
const transportData = computed(() =>
  sortGroup(transportCo2.value).map(([, val]) => Number(val.toFixed(2)))
)

// Add to series object for Apex Chart
const series = computed(() => [
  { name: 'Purchases', data: purchaseData },
  { name: 'Transport', data: transportData}])


function groupEmissionByDate(emissionsVar:string) {
  const grouped = new Map<string, number>()
  store.filteredData.value.forEach((row) => {
    const date = row.delivered_date
    const value = row[emissionsVar] ?? 0
    grouped.set(date, (grouped.get(date) || 0) + value)
  })
  return grouped
}

function sortGroup(group: Map) {
  return(Array.from(group.entries()).sort(([a], [b]) => a.localeCompare(b)))
}

</script>