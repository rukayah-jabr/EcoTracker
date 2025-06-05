<template>
  <div>
    <h1>Product Details</h1>
    <data-filter-group/>
    <ProductDetailsTable/>
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore'

const store = useDashboardStore()
console.log(store.rawData)

</script>