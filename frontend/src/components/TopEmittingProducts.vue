<template>
  <h2>Five products with highest emissions</h2>
  <ProductDetailsTable sortColumn="co2_total" :itemsPerPage="5" :hideFooter="true"/>
</template>

<style>
  h2 {
    text-align: center;
  }
</style>