<template>
  <h2 class="text-h6 text-center mb-3">Highest Emitting Products</h2>
  <ProductDetailsTable sortColumn="co2_total" :itemsPerPage="5" :hideFooter="true"/>
</template>

<style>

</style>