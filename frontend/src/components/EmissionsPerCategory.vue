<template>
  <div class="d-flex justify-space-between">
      <PieChart v-if="store.loaded" title="Product Emissions" :data="productEmissionsPerCategory" />
      <PieChart v-if="store.loaded" title="Transportation Emissions" :data="transportationEmissionsPerCategory" />
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore';

const store = useDashboardStore()

const productEmissionsPerCategory = computed(() => groupProductEmissionsByCategory(store.filteredData.value))
const transportationEmissionsPerCategory = computed(() => groupTransportationEmissionsByCategory(store.filteredData.value))

const categories = [
    "Haushaltsgeraete",
    "Kaffee & Zubehoer",
    "Reinigung & Waschmittel",
    "Batterien & Akkus",
    "Beleuchtung",
    "Elektronik",
    "Ersatzteile & Zubehoer",
    "Service",
    "Ersatzteile & Zubehoer",
    "Service",
    "Lieferservice",
    "Kuechengeraete"
]

function transformArrayToObject(categories: string[]): Record<string, number> {
  return categories.reduce((acc: Record<string, number>, category: string) => {
    acc[category] = 0;
    return acc;
  }, {})
}

function groupProductEmissionsByCategory(filteredData: any): Record<string, number> {
  const emissionsPerCategory = transformArrayToObject(categories)

  filteredData.forEach(product => {
    emissionsPerCategory[product.category] += product.co2_purchase
  })

  return emissionsPerCategory
}

function groupTransportationEmissionsByCategory(filteredData: any): Record<string, number> {
  const emissionsPerCategory = transformArrayToObject(categories)

  filteredData.forEach(product => {
    emissionsPerCategory[product.category] += product.co2_transport
  })

  return emissionsPerCategory
}

</script>