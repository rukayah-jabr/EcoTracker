<template>
    <v-row class="my-5">
        <v-col cols="4">
            <DateFilter :defaultRange=defaultRange></DateFilter>
        </v-col>
        <v-col cols="4">
            <CategoryFilter></CategoryFilter>
        </v-col>
    </v-row>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useDashboardStore } from '../stores/useDashboardStore'

const store = useDashboardStore()
const defaultRange = [new Date(store.filters.dateRange[0]), new Date(store.filters.dateRange[1])]

</script>