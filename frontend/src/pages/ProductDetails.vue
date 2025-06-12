<template>
  <div>
    <h1>Product Details</h1>
    <p class="font-italic mb-8">View product-level estimates calculated from your invoice data</p>
    <data-filter-group/>
    <div v-if="!store.loaded && !store.isLoading">
      <NoResults></NoResults>
    </div>
    <div v-else>
      <ProductDetailsTable/>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore'

const store = useDashboardStore()
console.log(store.rawData)

</script>