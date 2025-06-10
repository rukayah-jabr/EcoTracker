<template>
    <div class="my-3">
      <v-btn color="primary" @click="filterData" :loading="store.isLoading">
        Filter Data
      </v-btn>
    </div>
</template>
  
<script setup lang="ts">
import { useDashboardStore } from '../stores/useDashboardStore'
import { ref, onMounted } from 'vue'

const store = useDashboardStore()

async function filterData() {
    store.filterData()
}

</script>

<style scoped>

</style>