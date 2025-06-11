<template>
    <div class="my-3">
      <v-btn color="primary" @click="fetchData" :loading="store.isLoading">
        <span v-if=store.loaded>Reimport Data</span>
        <span v-else>Import Data</span>
      </v-btn>
      <div v-if="store.error && !store.isLoading" class="error">
        {{ store.error }}
      </div>
      <v-alert v-if="store.loaded && !store.error && !store.isLoading"
        color="success"
        icon="$success"
        title="Data successfully imported"
        text="Your purchase data has been successfully imported and calculated with emissions"
        class="mt-5"
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
  