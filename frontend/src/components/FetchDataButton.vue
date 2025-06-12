<template>
    <div class="my-3">
      <v-btn color="primary" @click="fetchData" :loading="store.isLoading">
        <span v-if=store.loaded>Reimport Data</span>
        <span v-else>Import Data</span>
      </v-btn>
      <v-alert v-if="store.error && !store.isLoading"
        color="error"
        icon="$error"
        :text="store.error"
        class="mt-5 w-xl-33 w-lg-50"
        variant="tonal"
      ></v-alert>
      <v-alert v-if="store.loaded && !store.error && !store.isLoading"
        color="success"
        icon="$success"
        text="Success! Your invoice data has been imported and estimated"
        class="mt-5 w-xl-33 w-lg-50"
        variant="tonal"
        ></v-alert>
    </div>
</template>
  
<script setup lang="ts">
import { useDashboardStore } from '../stores/useDashboardStore'
import { ref, onMounted } from 'vue'

const props = defineProps<{
  api: string
}>()

const store = useDashboardStore()

async function fetchData() {
    if (props.api) {
        store.apiEndpoint = props.api // set endpoint as text field value
        store.error = ''
        store.loadData()
    }
}

</script>

<style scoped>
.error {
  color: red;
  margin-top: 8px;
}
</style>
  