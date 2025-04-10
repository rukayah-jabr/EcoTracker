from dataclasses import dataclass
from datetime import date
from eco_tracker.distance_estimation.open_route_service import get_location_coordinates, get_route_distance
from eco_tracker.erp_integration.exceptions import CoordinatesNotFound, RouteDistanceFailed


class SupplierAddress:
    def __init__(self, street, city, state, zip, country):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip} {self.country}"
    
    def get_coordinates(self):
        coords = get_location_coordinates(str(self))
        if not coords:
            raise CoordinatesNotFound(str(self))
        return coords
    
    def get_distance_from_delivery_address(self, delivery_address: str):
        start = self.get_coordinates()
        end = get_location_coordinates(delivery_address)
        distance = None

        if start and end:
            if not start == end: # check if coordinates are the same
                distance = get_route_distance(start, end)
            else:
                distance = 0
        else:
            raise CoordinatesNotFound(delivery_address)
        
        if distance == None:
            raise RouteDistanceFailed(start, end)
        
        return distance

    
@dataclass
class ProductPurchase:
    delivered_date: date
    description: str
    unit: str
    quantity: int
    unit_price: float
    supplier: str
    supplier_address: SupplierAddress