<template>
  <div>
    <v-select
    clearable
    chips
    label="Filter category"
    :items="displayCategories"
    v-model="store.filters.category"
    multiple
    @update:modelValue="onCategoryChange(store.filters.category)"
    ></v-select>
  </div>
</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore'
import { ref, onMounted } from 'vue'

const selectedCategories = ref([])

const store = useDashboardStore()
const displayCategories = [...new Set(store.rawData.map(item => item.category))].sort();


function onCategoryChange(selectedCategories:Array<string>) {
  store.updateFilter('category', selectedCategories)
}
</script>