<template>
  <v-slider
    v-model="store.filters.confidence"
    :max="1"
    :min="0"
    :step="0.1"
    thumb-label="always"
    color="primary"
    label="Confidence Level"
    @update:modelValue="onConfidenceChange(store.filters.confidence)"
  ></v-slider>

</template>

<script lang="ts" setup>
import { useDashboardStore } from '../stores/useDashboardStore'
import { ref, onMounted } from 'vue'

const store = useDashboardStore()

function onConfidenceChange(confidence: number) {
    store.updateFilter('confidence', confidence)
}
</script>