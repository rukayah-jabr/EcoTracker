<template>
  <div>
    <h1>Data Dashboard</h1>
    <data-filter-group/>
    <emissions-over-time></emissions-over-time>
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore'
import { ref, onMounted } from 'vue'

const store = useDashboardStore()

</script>
