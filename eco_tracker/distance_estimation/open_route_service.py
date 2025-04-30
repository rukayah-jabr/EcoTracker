import os
import openrouteservice
from dotenv import load_dotenv
from eco_tracker.distance_estimation import exceptions

# Load environment variables from the .env file
load_dotenv()
API_KEY = os.getenv("OPEN_ROUTE_SERVICE_API_KEY")

client = openrouteservice.Client(key=API_KEY)

def get_route_distance(start, end):
    """
    Calculates the distance (in meters) between two coordinates.

    :param start: Tuple (longitude, latitude) for the starting point
    :param end: Tuple (longitude, latitude) for the destination point
    :return: Distance in kilometers
    """
    try:
        route = client.directions(
            coordinates=[start, end],
            profile='driving-car',  # Alternatives: 'cycling-regular', 'foot-walking', etc.
            format='geojson'
        )
        distance_meters = route['features'][0]['properties']['segments'][0]['distance']
        return distance_meters / 1000  # Convert meters to kilometers
    except Exception:
        raise exceptions.RouteDistanceFailed(start, end)
    
def get_location_coordinates(address:str):
    """
    Returns the coordinates of a given address

    :param address: String for the address
    :return: List of coordinates, latitude and longitude
    """
    try:
        geocode = client.pelias_search(text=address)

        if len(geocode['features']) < 3: # only calculate accurate address with 1-2 addresses
            coords = geocode['features'][0]['geometry']['coordinates']
            return coords
        else:
            raise exceptions.CoordinatesNotFound(address)
    except Exception:
        raise exceptions.CoordinatesNotFound(address)
    
def get_distance_from_delivery_address(supplier_address: str, delivery_address: str):
    """
    Returns the distance between supplier and delivery address by
    determining location coordations then calculating the route distance

    :param supplier_address: String for the supplier's address
    :param delivery_address: String for the company's delivery address
    :return: Distance in kilometers
    """
    start = get_location_coordinates(supplier_address)
    end = get_location_coordinates(delivery_address)
    distance = None

    if start and end:
        if not start == end: # check if coordinates are the same
            distance = get_route_distance(start, end)
        else:
            distance = 0
    else:
        raise exceptions.CoordinatesNotFound(delivery_address)
    
    if distance == None:
        raise exceptions.RouteDistanceFailed(start, end)
    
    return distance
