import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchEmissionsData } from '@/services/dataService'
import type { EmissionsDataRecord } from '../types/emissionsDataRecord'
import { formatDateToYMD } from '@/utils/dateHelpers'

export const useDashboardStore = defineStore('dashboard', () => {
  const api_endpoint = ref('')
  const rawData = ref<EmissionsDataRecord[]>([])
  const filters = ref({
    dateRange: [ new Date(2024, 7, 2), new Date(2024, 7, 2) ], // month index is 1 off from actual month
    category: null,
  })
  const isLoading = ref(false)
  const loaded = ref(false)
  const error = ref('')

  async function loadData() {
    isLoading.value = true
    if (!api_endpoint) {
      error.value = "No API endpoint set"
      return
    }
    console.log("API: " + api_endpoint.value)

    let start = formatDateToYMD(filters.value.dateRange[0])
    let end = formatDateToYMD(filters.value.dateRange[filters.value.dateRange.length - 1]) // uses last value in dynamic range
    
    console.log("Setting date range: " + start + " to " + end)

    try {
      // http://localhost:8069
      const fetchUrl = api_endpoint.value + "&start_date=" + start + "&end_date=" + end
      rawData.value = await fetchEmissionsData(fetchUrl)
      console.log(rawData.value)
    }
    catch(err: any) {
      error.value = err.message || 'Failed to fetch data'
    }
    finally {
      isLoading.value = false
      loaded.value = true
    }
  }

  function updateFilter(key, value) {
    filters.value[key] = value
  }

  const filteredData = computed(() => {
    return rawData.value.filter(item => {
      const withinDate =
        (!filters.value.dateRange[0] || new Date(item.delivered_date) >= new Date(filters.value.dateRange[0])) &&
        (!filters.value.dateRange[1] || new Date(item.delivered_date) <= new Date(filters.value.dateRange[1]))
      const matchesCategory =
        !filters.value.category || item.category === filters.value.category
      return withinDate && matchesCategory
    })
  })

  return { api_endpoint, rawData, filteredData, filters, loadData, updateFilter, isLoading, loaded, error }
})
