import os

import openrouteservice
from dotenv import load_dotenv

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
    except Exception as e:
        print("Error:", e)
        return None
    
def get_location_coordinates(address):
    """
    Returns the coordinates of a given address

    :param address: String for the address
    :return: List of coordinates, latitude and longitude
    """
    try:
        geocode = client.pelias_search(text=address)
        coords = geocode['features'][0]['geometry']['coordinates']
        return coords
    except Exception as e:
        print("Error:", e)
        return None


# Example
# start_coords = get_location_coordinates("Mitterfeldstraße 7, Amstetten, None 3300 AT") # Supplier address
# end_coords = get_location_coordinates("Stadtwerkestr. 2 Amstetten 3300 AT")  # Amstetten Stadtwerke address

# if start_coords and end_coords:
#     distance = get_route_distance(start_coords, end_coords)

# if distance:
#     print(f"The distance is approximately {distance:.2f} km")
