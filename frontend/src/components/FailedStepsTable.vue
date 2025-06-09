<template>
  <div v-if="store.loaded && !store.isLoading">
      <!-- Temporary display of results for now -->
      <h3 class="mt-8">Pipeline Steps:</h3>
      <v-table>
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
          <tr v-for="record in store.rawData" :key="record.description">
            <td>{{ record.description }} <em>(Qty: {{ record.quantity }})</em></td>
            <td><b>{{ record.co2_purchase.toFixed(3) }}</b></td>
            <td><b>{{ record.co2_transport.toFixed(3) }}</b></td>
            <td v-for="(value, key) in record.failed_steps" :key="key">
               <component :is="getStepStatusIcon(value)"/>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>
</template>
  
<script setup lang="ts">
import { ref, h, computed } from 'vue'
import { VIcon } from 'vuetify/components'
import { useDashboardStore } from '../stores/useDashboardStore'

const store = useDashboardStore()

function getStepStatusIcon(value:boolean) {
  // Set success to true if step did not fail (e.g. failedStep == false)
  const iconName = value == false ? 'mdi-check-circle' : 'mdi-close-circle'
  const iconColor = value == false ? 'green' : 'red'

  return h(VIcon, { icon: iconName, color: iconColor })
}

// Manual function to format date since using .toISOString causes issues (using day before)
function formatDateToYMD(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0') // Months are 0-based
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
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
  