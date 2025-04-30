from dataclasses import dataclass
from datetime import date

from eco_tracker.emission_factors.emission_factors_interface import EmissionFactor

class SupplierAddress:
    def __init__(self, street: str, city: str, state:str, zip:str, country:str):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip} {self.country}"
    
# This is the element that is passed from one step to the next in the pipeline
# TODO: Correct the types to the most specific ones e.g. status should be an enum
@dataclass
class Product:
	# Data from the original database
	delivered_date: date
	description: str
	unit: str
	quantity: float
	price: float # TODO: change to 'unit_price'
	supplier: str
	supplier_address: SupplierAddress
	# Data created by the pipeline
	climatiq_categories: list[str] # TODO: change name to 'estimate_categories'
	category: str # TODO: Change to an enum and change name to 'display_category'
	emission_factor: EmissionFactor
	delivery_distance: float
	co2e: float # TODO: change name to co2_purchase
	co2_transport: float


@dataclass
class Supplier:
	id: int
	name: str
	country: str
	postal_code: str
	city: str
	address: str
