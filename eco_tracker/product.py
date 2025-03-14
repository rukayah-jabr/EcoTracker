from dataclasses import dataclass

from eco_tracker.emission_factors.emission_factors_interface import EmissionFactor

# This is the element that is passed from one step to the next in the pipeline
# TODO: Correct the types to the most specific ones e.g. status should be an enum
@dataclass
class Product:
	# Data from the original database
	description: str
	unit: str
	quantity: float
	price: int
	status: str
	# Data created by the pipeline
	climatiq_categories: list[str]
	category: str # TODO: Change to an enum
	emission_factor: EmissionFactor
	co2e: float


@dataclass
class Supplier:
	id: int
	name: str
	country: str
	postal_code: str
	city: str
	address: str
