from dataclasses import dataclass
from datetime import date
from eco_tracker.emission_factors.emission_factors_interface import EmissionFactor

class SupplierAddress:
    def __init__(self, street, city, state, zip, country):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip} {self.country}"
    
@dataclass
class ProductPurchase:
    delivered_date: date
    description: str
    unit: str
    quantity: int
    unit_price: float
    supplier: str
    supplier_address: SupplierAddress