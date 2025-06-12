<template>
  <div>
    <h1>Data Dashboard</h1>
    <p class="font-italic mb-8">Analyze the results of your emission estimates</p>
    <data-filter-group/>
    <div v-if="!store.loaded && !store.isLoading">
      <NoResults></NoResults>
    </div>
    <emissions-over-time></emissions-over-time>
    <div class="my-10"></div>
    <emissions-per-category></emissions-per-category>
    <div class="my-10"></div>
    <top-emitting-products></top-emitting-products>
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from "../stores/useDashboardStore";

const store = useDashboardStore();
</script>
