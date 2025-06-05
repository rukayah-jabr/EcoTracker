<template>
  <div>
    <v-date-input
      v-model="dateRange"
      label="Select date range"
      max-width="368"
      multiple="range"
      class="mr-5"
      :oninput="onDateChange(dateRange)"
    ></v-date-input>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useDashboardStore } from '../stores/useDashboardStore'
import { formatDateToYMD } from '../utils/dateHelpers'

const props = defineProps<{
  defaultRange: Array<Date>,
}>()

const store = useDashboardStore()

// set range to provided default
const dateRange = ref(props.defaultRange)

function onDateChange(newRange:Array<Date>) {
  let start = formatDateToYMD(newRange[0])
  let end = formatDateToYMD(newRange[newRange.length - 1]) // uses last value in dynamic range

  store.updateFilter('dateRange', [start, end])
}
</script>