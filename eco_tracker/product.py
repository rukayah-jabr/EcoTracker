from dataclasses import dataclass
from datetime import date


@dataclass
class FailedSteps:
	estimate_categories: bool
	emission_factor_fetching: bool
	purchase_co2_calculation: bool
	distance_estimation: bool
	weight_estimation: bool
	delivery_emissions_estimation: bool

class Address:
	def __init__(self, street: str, city: str, zip:str, country:str):
		self.street = street
		self.city = city
		self.zip = zip
		self.country = country

	def __str__(self):
		return f"{self.street}, {self.zip} {self.city}, {self.country}"

# Lieferung
@dataclass
class Delivery:
	def __init__(self, id: int, name: str, type: str, partner_name: str):
		self.id = id
		self.name = name
		self.type = type
		self.partner_name = partner_name

@dataclass
class EmissionFactor:
	co2e: float
	co2e_unit: str
	activity_unit: str
	name: str
	description: str    

# This is the element that is passed from one step to the next in the pipeline
# TODO: Correct the types to the most specific ones e.g. status should be an enum
@dataclass
class Product:
	# Data from the original database
	delivered_date: date
	description: str
	unit: str
	quantity: float
	unit_price: float
	supplier: str
	supplier_address: Address
	delivery_address: Address
	delivery: Delivery | None
	# Data created by the pipeline
	estimated_categories: list[str]
	estimated_matched_category: str | None
	category: str | None # TODO: Change to an enum
	emission_factor: EmissionFactor | None
	delivery_emission_factor: EmissionFactor | None
	delivery_distance: float | None
	delivery_transportation_type: str | None
	weight: float | None # in kg
	co2_purchase: float | None
	co2_transport: float | None
	failed_steps: FailedSteps
	confidence: float | None
