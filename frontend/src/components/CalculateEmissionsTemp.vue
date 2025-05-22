<template>
  <v-container>
    <h3 class="border-t pt-5">Temporary test of API fetch and and data return</h3>
    <ul class="ml-5 my-3">
      <li><b>2024-08-02</b> to <b>2024-08-02:</b> 2 entries</li>
      <li><b>2024-08-02</b> to <b>2024-08-05:</b> 3 entires</li>
      <li><b>2024-08-02</b> to <b>2024-08-08:</b> 9 entries</li>
    </ul>

    <div class="d-flex mt-5">
      <v-date-input
      v-model="dateRange"
      label="Select range"
      max-width="368"
      multiple="range"
      class="mr-5"
    ></v-date-input>
    <div class="my-3">
      <v-btn color="primary" @click="loadData" :loading="loading">
        Calculate Emissions (Test)
      </v-btn>
  
      <div v-if="error" class="error">
        {{ error }}
      </div>
    </div>
    </div>
    <div>
      <!-- Temporary display of results for now -->
      <v-table v-if="records.length">
        <thead>
          <tr>
            <th width='300'>
              Product
            </th>
            <th>
              <b>CO2 Estimate: Purchase</b>
            </th>
            <th>
              <b>CO2 Estimate: Transportation</b>
            </th>
            <th>
              Categorized
            </th>
            <th>
              CO2 Factor Found
            </th>
            <th>
              Purchase CO2
            </th>
            <th>
              Distance Estimated
            </th>
            <th> 
              Weight Estimated
            </th>
            <th>
              Transportation CO2
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in records" :key="record.description">
            <td>{{ record.description }} <em>(Qty: {{ record.quantity }})</em></td>
            <td><b>{{ record.co2_purchase.toFixed(3) }}</b></td>
            <td><b>{{ record.co2_transport.toFixed(3) }}</b></td>
            <td v-for="(value, key) in record.failed_steps" :key="key">
              <!-- Did the step succeed? (failed = false) -->
               <component :is="getStepStatusIcon(value)"/>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>
  </v-container>
</template>
  
<script setup lang="ts">
import { ref, h } from 'vue'
import { fetchEmissionsData } from '../services/dataService'
import type { EmissionsDataRecord } from '../types/emissionsDataRecord'
import { VIcon } from 'vuetify/components'

const loading = ref(false)
const error = ref('')
const records = ref<EmissionsDataRecord[]>([])

// Initial date values
const initialStart = new Date('2024-08-02')
const initialEnd = new Date('2024-08-02')

const dateRange = ref<Date[]>([initialStart, initialEnd])

async function loadData() {
  loading.value = true
  error.value = ''
  const start = dateRange.value[0].toISOString().split('T')[0]
  const end = dateRange.value[dateRange.value.length - 1].toISOString().split('T')[0]
  console.log(start + " - " + end)

  try {
    const fetchUrl = "http://localhost:8069" + "&start_date=" + start + "&end_date=" + end
    records.value = await fetchEmissionsData(fetchUrl)
  } catch (err: any) {
    error.value = err.message || 'Failed to fetch data'
  } finally {
    loading.value = false
    console.log(records)
    console.log(records.value)
  }
}

function getStepStatusIcon(value:boolean) {
  // Set success to true if step did not fail (e.g. failedStep == false)
  const iconName = value == false ? 'mdi-check-circle' : 'mdi-close-circle'
  const iconColor = value == false ? 'green' : 'red'

  return h(VIcon, { icon: iconName, color: iconColor })
}
</script>

<style scoped>
.error {
  color: red;
  margin-top: 8px;
}

table th {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: .15em;
  padding: 10px!important;
}

table td {
  padding: 10px!important;
}
</style>
  