import json
from typing import Any

import openrouteservice
from geopy.distance import geodesic

from eco_tracker import api_cache
from eco_tracker.distance_estimation import exceptions
from eco_tracker.distance_estimation.distance_estimation_interface import DistanceEstimator


class OpenRouteService(DistanceEstimator):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client: openrouteservice.Client = openrouteservice.Client(key=self.api_key)

    def get_route_distance(self, start: tuple[float, float], end: tuple[float, float]) -> float:
        """
        Calculates the distance (in meters) between two coordinates.

        :param start: Tuple (longitude, latitude) for the starting point
        :param end: Tuple (longitude, latitude) for the destination point
        :return: Distance in kilometers
        """

        @api_cache.execute_or_get_from_cache(url="open_route_service.directions", request=json.dumps({"start":start, "end":end}))
        def fetch_distance(coordinates: list) -> float:
            try:
                route = self.client.directions( # type: ignore
                    coordinates=coordinates,
                    profile='driving-car',  # Alternatives: 'cycling-regular', 'foot-walking', etc.
                    format='geojson'
                )
                distance_meters = route['features'][0]['properties']['segments'][0]['distance']
                return distance_meters / 1000  # Convert meters to kilometers
            except Exception:
                raise exceptions.RouteDistanceFailed(start, end)
        
        return fetch_distance([start, end])

    def get_location_coordinates(self, address: str) -> tuple[float, float]:
        """
        Returns the coordinates of a given address

        :param address: String for the address
        :return: List of coordinates, latitude and longitude
        """
        @api_cache.execute_or_get_from_cache(url="open_route_service.pelias_search", request=address)
        def fetch_coords(address: str) -> dict[str, Any]:
            try:
                return self.client.pelias_search(text=address) # type: ignore
            except exceptions.ManyMatchingCoordinatesFound as e:
                raise e
            except Exception as e:
                raise exceptions.CoordinatesNotFound(address)
        
        geocode: dict[str, Any] = fetch_coords(address)
        
        if len(geocode.get('features', [])) == 0:
            raise exceptions.CoordinatesNotFound(address)
            
        chosen_coords: tuple | None = None
        for location in geocode.get('features', []):
            if location['properties']['confidence'] < 0.7:
                continue
            
            cur_coords = location['geometry']['coordinates']
            
            if chosen_coords is None:
                chosen_coords = cur_coords
                continue 

            distance_between_matching_coords = self.get_distance_between_coordinates(chosen_coords, cur_coords)
            if distance_between_matching_coords > 10:
                raise exceptions.ManyMatchingCoordinatesFound(address=address)
        
        if chosen_coords is None:
            raise exceptions.CoordinatesNotFound(address)
        
        return chosen_coords
    
    def get_distance_between_coordinates(self, start: tuple[float, float], end: tuple[float, float]) -> float:
        """
        Returns the straight line distance between two coordinates
        """
        start_reordered: tuple = (start[1], start[0])
        end_reordered: tuple = (end[1], end[0])
        return geodesic(start_reordered, end_reordered).km
        
    def get_distance_from_delivery_address(self, supplier_address: str, delivery_address: str) -> float:
        """
        Returns the distance between supplier and delivery address by
        determining location coordations then calculating the route distance

        :param supplier_address: String for the supplier's address
        :param delivery_address: String for the company's delivery address
        :return: Distance in kilometers
        """
        start = self.get_location_coordinates(supplier_address)
        end = self.get_location_coordinates(delivery_address)
        distance = None

        if start and end:
            if start != end: # check if coordinates are the same
                distance = self.get_route_distance(start, end)
            else:
                distance = 0
        else:
            raise exceptions.CoordinatesNotFound(delivery_address)
        
        if distance == None:
            raise exceptions.RouteDistanceFailed(start, end)
        
        return distance
