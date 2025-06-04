<!-- components/BarChart.vue -->
<template>
  <v-card>
    <v-card-title>{{ props.title }}</v-card-title>
    <v-card-text>
      <ApexChart type="bar" :options="chartOptions" :series="series" height="350" />
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { ApexOptions } from 'apexcharts'

const props = defineProps<{
  title: string,
  series: [],
  xaxis: []
}>()

const series = ref(props.series)

// const series = ref([
//   {
//     name: '2024',
//     data: [44, 55, 41, 67, 22, 43]
//   },
//   {
//     name: '2025',
//     data: [53, 32, 33, 52, 13, 44]
//   }
// ])

const chartOptions = ref<ApexOptions>({
  chart: {
    type: 'bar',
    height: 350,
    stacked: true
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '55%',
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    show: true,
    width: 2,
    colors: ['transparent']
  },
  xaxis: {
    categories: props.xaxis
  },
  yaxis: {
    title: {
      text: 'CO2 Emissions'
    }
  },
  fill: {
    opacity: 1
  },
  tooltip: {
    y: {
      formatter: function (val: number) {
        return `${val.toFixed(2)}`
      }
    }
  }
})
</script>
