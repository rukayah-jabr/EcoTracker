<template>
  <div>
    <h1 class="mb-8">Data Dashboard</h1>
    <data-filter-group/>
    <emissions-over-time></emissions-over-time>
    <div class="my-10"></div>
    <emissions-per-category></emissions-per-category>
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore';

const store = useDashboardStore()

</script>
