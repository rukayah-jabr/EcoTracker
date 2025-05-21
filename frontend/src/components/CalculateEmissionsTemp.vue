<template>
  <v-container max-width="900">
    <p>Temporary Test of API fetch and and data return:</p>
    <div class="my-3">
      <v-btn color="primary" @click="loadData" :loading="loading">
        Calculate Emissions (Test)
      </v-btn>
  
      <div v-if="error" class="error">
        {{ error }}
      </div>
  
      <!-- Temporary display of results for now -->
      <v-table v-if="records.length">
        <thead>
          <tr>
            <th>
              Product
            </th>
            <th>
              CO2 Emissions: Purchase
            </th>
            <th>
              CO2 Emissions: Transportation
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in records" :key="record.description">
            <td>{{ record.description }}</td>
            <td>{{ record.co2_purchase }}</td>
            <td>{{ record.co2_transport }}</td>
          </tr>
        </tbody>
      </v-table>
    </div>
  </v-container>
</template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { fetchEmissionsData } from '../services/dataService'
  import type { EmissionsDataRecord } from '../types/emissionsDataRecord'
  
  const loading = ref(false)
  const error = ref('')
  const records = ref<EmissionsDataRecord[]>([])
  
  async function loadData() {
    loading.value = true
    error.value = ''
    try {
      records.value = await fetchEmissionsData("http://localhost:8069&start_date=2024-08-02&end_date=2024-08-02")
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch data'
    } finally {
      loading.value = false
      console.log(records)
      console.log(records.value)
    }
  }
  </script>
  
  <style scoped>
  .error {
    color: red;
    margin-top: 8px;
  }
  </style>
  