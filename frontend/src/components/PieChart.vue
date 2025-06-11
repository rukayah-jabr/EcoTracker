<template>
  <v-card class="pie-chart-card">
    <v-card-title>{{ props.title }}</v-card-title>
    <v-card-text>
      <ApexChart width="100%" type="pie" :options="chartOptions" :series="series"/>
    </v-card-text>
  </v-card>
</template>


<script setup lang="ts">

import type { ApexOptions } from 'apexcharts';

const props = defineProps<{
  title: string,
  data: Record<string, number>
}>()

const chartOptions = ref<ApexOptions>({
  chart: {
    id: 'vuechart-example',
  },
  labels: Object.keys(props.data)
})

const series = computed(() => Object.values(props.data))

</script>

<style scoped>
.pie-chart-card {
  width: 48%;
  max-width: 100%;
}
</style>