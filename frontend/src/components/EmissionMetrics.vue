<template>
  <div class="mb-10">
      <v-row>
        <v-col cols="12" md="4" v-for="(value, key) in metrics" :key="key">
            <v-card variant="flat" class="text-center py-5">
                <v-card-title class="text-overline">{{ key }}</v-card-title>
                <v-card-text class="text-h4 font-weight-light">{{ value }}</v-card-text>
            </v-card>
        </v-col>
      </v-row>
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore'
import { computed, ref } from 'vue'

const store = useDashboardStore()

// Sum up emissions data
const purchaseCo2 = computed(() => totalSumEmissions("co2_purchase"))
const transportCo2 = computed(() => totalSumEmissions("co2_transport"))
const totalCo2 = computed(() => totalSumEmissions("co2_total"))

// Combine into metrics object
const metrics = computed(() => {
    return {
    "Total CO₂ Emissions": totalCo2.value.toFixed(2),
    "From Purchases": calculatePercent(purchaseCo2.value, totalCo2.value),
    "From Delivery": calculatePercent(transportCo2.value, totalCo2.value),
    }
})

function totalSumEmissions(emissionsVar:string) {
  let sum = 0
  store.filteredData.value.forEach((row) => {
    sum += row[emissionsVar]
  })
  return sum
}

function calculatePercent(numerator, denominator) {
  const div = numerator/denominator
  if (div) {
    const perc = (div*100).toFixed(2)
    return (perc + "%")
  }
  else {
    return "–%"
  }
}

</script>

<style scoped>


</style>