import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fetchEmissionsData } from '@/services/dataService'
import type { EmissionsDataRecord } from '../types/emissionsDataRecord'
import { formatDateToYMD } from '../utils/dateHelpers'

export const useDashboardStore = defineStore('dashboard', () => {
  const apiEndpoint = ref('http://localhost:8069')
  const rawData = ref<EmissionsDataRecord[]>([])
  const filters = ref({
    dateRange: [ new Date(2024, 7, 2), new Date(2024, 7, 2) ], // month index is 1 off from actual month
    category: null,
  })
  const filteredData = ref<EmissionsDataRecord[]>([])
  const isLoading = ref(false)
  const loaded = ref(false)
  const error = ref('')

  async function loadData() {
    isLoading.value = true
    if (!apiEndpoint) {
      error.value = "No API endpoint set"
      return
    }

    let start = filters.value.dateRange[0]
    let end = filters.value.dateRange[1] // uses last value in dynamic range
    
    console.log("Setting date range: " + start + " to " + end)

    try {
      // http://localhost:8069
      const fetchUrl = apiEndpoint.value + "&start_date=" + start + "&end_date=" + end
      rawData.value = await fetchEmissionsData(fetchUrl)
      
      // Add computed fields
      rawData.value = rawData.value.map(item => ({
        ...item,
        co2_total: item.co2_purchase + item.co2_transport,
        date: new Date(item.delivered_date)
      }));

      console.log(rawData.value)
      filterData()
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

  function filterData() {
    filteredData.value = computed(() => {
      return rawData.value.filter(item => {
        const withinDate =
          (!filters.value.dateRange[0] || new Date(item.delivered_date) >= new Date(filters.value.dateRange[0])) &&
          (!filters.value.dateRange[1] || new Date(item.delivered_date) <= new Date(filters.value.dateRange[1]))
        const matchesCategory =
          !filters.value.category || item.category === filters.value.category
        return withinDate && matchesCategory
      })
    })
  }


  return { apiEndpoint, rawData, filteredData, filters, loadData, updateFilter, filterData, isLoading, loaded, error }
})
