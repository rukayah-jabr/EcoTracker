<template>
  <div>
    <h1>Product Details</h1>
    <v-data-table :items="store.rawData" :headers="headers">
        <template v-slot:item.category="{ value }">
            <v-chip
            color="secondary"
            variant="outlined"
            :text="value"></v-chip>
        </template>
        <template v-slot:item.co2_purchase="{ item }">
            <template v-if="item.failed_steps.purchase_co2_calculation">
                <v-chip
                prepend-icon="mdi-alert"
                color="orange"
                dark
                >
                Could not estimate
                </v-chip>
            </template>
            <template v-else>
                {{ item.co2_purchase.toFixed(4) }}
            </template>
        </template>
        <template v-slot:item.co2_transport="{ item }">
            <template v-if="item.failed_steps.delivery_emissions_estimation">
                <v-chip
                prepend-icon="mdi-alert"
                color="orange"
                dark
                >
                Could not estimate
                </v-chip>
            </template>
            <template v-else>
                {{ item.co2_transport.toFixed() }}
            </template>
        </template>
        <template v-slot:item.co2_total="{ value }">
            <v-chip
            :color="getEmissionsColor(value)"
            :text="(value).toFixed(4)"></v-chip>
        </template>
    </v-data-table>
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore'

const store = useDashboardStore()
console.log(store.rawData)

const headers = [
    { title: 'Date', key: 'delivered_date', sortable: true},
    { title: 'Product', value: 'description', sortable: true},
    { title: 'Quantity', value: 'quantity', align: 'center'},
    { title: 'Category', value: 'category', align: 'center', sortable: true},
    { 
        title: 'CO2 Emissions',
        align: 'center',
        children: [
            { title: 'Purchase', value: 'co2_purchase', align: 'center', sortable: true},
            { title: 'Transportation', value: 'co2_transport', align: 'center', sortable: true},
            { title: 'Total', value: 'co2_total', align: 'center', sortable: true}
        ]
    }
]

function getEmissionsColor (emissions:number) {
    // TODO: make this more dynamic/relative according to actual data
    if (emissions > 100) return 'red'
    else if (emissions > 50) return 'orange'
    else return 'green'
  }

function getFailedResultFlag (failedStep:boolean) {
    if (!failedStep) {
        return {
            color: "orange",
            icon: "mdi-alert"
        };
    }
    return null;
}

</script>