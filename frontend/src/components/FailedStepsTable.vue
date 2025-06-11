<template>
  <div v-if="store.loaded && !store.isLoading">
      <!-- Temporary display of results for now -->
       <div class="mt-8 mb-4 border-t pt-5">
        <h3>Pipeline Steps (dev/demo purposes)</h3>
        <p><em>The table below displays the outcome of various steps within the estimation pipeline</em></p>
       </div>
      <v-table>
        <thead>
          <tr>
            <th width='300'>
              Product
            </th>
            <th>
              CO₂ Estimate: Purchase
            </th>
            <th>
              CO₂ Estimate: Transportation
            </th>
            <th>
              Categorized
            </th>
             <th>
              Reordered
            </th>
            <th>
              CO2 Factor Found
            </th>
            <th>
              Purchase CO₂
            </th>
            <th>
              Distance Estimated
            </th>
            <th> 
              Weight Estimated
            </th>
            <th>
              Delivery CO₂
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in store.rawData" :key="record.description">
            <td>{{ record.description }} <em>(Qty: {{ record.quantity }})</em></td>
            <td>{{ record.co2_purchase.toFixed(3) }}</td>
            <td>{{ record.co2_transport.toFixed(3) }}</td>
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
  const iconColor = value == false ? 'success' : 'error'

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
  font-size: 12px;
  padding: 10px!important;
}

table td {
  padding: 10px!important;
}
</style>
  