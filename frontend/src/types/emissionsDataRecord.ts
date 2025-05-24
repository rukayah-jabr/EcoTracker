export interface Address {
    street: string
    city: string
    zip: string
    country: string
  }
  
  export interface EmissionFactor {
    co2e: number
    co2e_unit: string
    activity_unit: string
    name: string
    description: string
  }
  
  export interface FailedSteps {
    estimate_categories: boolean
    emission_factor_fetching: boolean
    purchase_co2_calculation: boolean
    distance_estimation: boolean
    weight_estimation: boolean
    delivery_emissions_estimation: boolean
  }
  
  export interface EmissionsDataRecord {
    delivered_date: string
    description: string
    unit: string
    quantity: number
    unit_price: number
    supplier: string
    supplier_address: Address
    delivery_address: Address
    climatiq_categories: string[]
    climatiq_matched_category: string
    category: string | null
    emission_factor: EmissionFactor
    delivery_emission_factor: EmissionFactor
    delivery_distance: number
    delivery_transportation_type: string | null
    weight: number
    co2_purchase: number
    co2_transport: number
    failed_steps: FailedSteps
  }