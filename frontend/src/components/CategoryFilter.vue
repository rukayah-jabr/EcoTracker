<template>
  <div>
    <v-select
    clearable
    chips
    label="Select"
    :items="displayCategories"
    :v-model="selectedCategories"
    multiple
    :oninput="onCategoryChange(selectedCategories)"
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