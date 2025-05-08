from dataclasses import dataclass
from datetime import date

from eco_tracker.emission_factors.emission_factors_interface import EmissionFactor


@dataclass
class FailedSteps:
	estimate_categories: bool
	emission_factor_fetching: bool
	purchase_co2_calculation: bool
	distance_estimation: bool
    
class Address:
	def __init__(self, street: str, city: str, zip:str, country:str):
		self.street = street
		self.city = city
		self.zip = zip
		self.country = country

	def __str__(self):
		return f"{self.street}, {self.zip} {self.city}, {self.country}"
    
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
	# Data created by the pipeline
	climatiq_categories: list[str] # TODO: change name to 'estimate_categories'
	climatiq_matched_category: str | None # TODO: change name to 'estimate_matched_category'
	category: str | None # TODO: Change to an enum
	emission_factor: EmissionFactor | None
	delivery_distance: float | None
	co2_purchase: float | None
	co2_transport: float | None
	failed_steps: FailedSteps
