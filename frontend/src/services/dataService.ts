import type { EmissionsDataRecord } from '@/types/emissionsDataRecord'
import axios from 'axios'

// Fetch all records
export async function fetchEmissionsData(url_parameter:string): Promise<EmissionsDataRecord[]> {
  console.log("Fetching emissions data... " + url_parameter)
  const response = await axios.get<EmissionsDataRecord[]>(`/api/calculate-emissions?url=${url_parameter}`)
  return response.data
}