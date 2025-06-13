<template>
  <div>
    <v-data-table
    :items="store.filteredData.value"
    :headers="headers"
    :sort-by="[{ key: sortColumn, order: 'desc' }]"
    :items-per-page="itemsPerPage"
    :hide-default-footer="hideFooter"
    color="primary"
    hover
    >
        <template v-slot:item.category="{ value }">
            <v-chip
            color="primary"
            :text="value"
            label></v-chip>
        </template>
        <template v-slot:item.co2_purchase="{ item }">
            <template v-if="item.failed_steps.purchase_co2_calculation">
                <v-chip
                prepend-icon="mdi-alert"
                color="warning"
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
                color="warning"
                dark
                >
                Could not estimate
                </v-chip>
            </template>
            <template v-else>
                {{ item.co2_transport.toFixed(4) }}
            </template>
        </template>
        <template v-slot:item.co2_total="{ value }">
            <v-chip
            :color="getEmissionsColor(value)"
            :text="(value).toFixed(4)"></v-chip>
        </template>
        <template v-slot:item.emission_factor="{ item }">
            <v-tooltip location="top" max-width="920">
                <template v-slot:activator="{ props }">
                    <v-btn
                        v-bind="props"
                        icon
                        color="primary"
                        size="medium"
                        class="rounded-circle"
                        variant="plain"
                    >
                        <v-icon>mdi-information</v-icon>
                    </v-btn>
                </template>
                <span><span class="text-overline">Matched purchase emission factor:</span><br><b>{{ item?.emission_factor?.name}}</b> <br> {{ item?.emission_factor?.description }}</span>
            </v-tooltip>
        </template>
    </v-data-table>
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore'

const props = withDefaults(defineProps<{
  sortColumn?: string
  itemsPerPage?: number
  hideFooter?: boolean
}>(), {
  sortColumn: 'delivered_date',
  itemsPerPage: 10,
  hideFooter: false
})

const store = useDashboardStore()

const headers = [
    { title: 'Date', key: 'delivered_date', sortable: true},
    { title: 'Product', value: 'description', sortable: true},
    { title: 'Quantity', value: 'quantity', align: 'center'},
    { title: 'Category', value: 'category', align: 'center', sortable: true},
    { title: 'Purchase CO₂ Estimate', value: 'co2_purchase', align: 'center', sortable: true},
    { title: 'Delivery CO₂ Estimate', value: 'co2_transport', align: 'center', sortable: true},
    { title: 'Total CO₂ Estimate', value: 'co2_total', align: 'center', sortable: true},
    { title: '', value: 'emission_factor', align: 'center', sortable: false},
]

function getEmissionsColor (emissions:number) {
    // TODO: make this more dynamic/relative according to actual data
    if (emissions > 100) return 'error'
    else if (emissions > 50) return 'orange'
    else if (emissions < 0) return 'green'
    else return 'success'
  }

</script>