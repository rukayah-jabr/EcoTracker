import os
from unittest.mock import patch

import pytest
from dotenv import load_dotenv

from eco_tracker.distance_estimation import exceptions
from eco_tracker.distance_estimation.open_route_service.open_route_service import OpenRouteService


@pytest.fixture
def open_route_service():
    load_dotenv()
    api_key = os.getenv("OPEN_ROUTE_SERVICE_API_KEY")
    if not api_key:
        pytest.skip("OPEN_ROUTE_SERVICE_API_KEY not found in environment variables")
    return OpenRouteService(api_key=api_key)


def test_openrouteservice_instance(open_route_service):
    assert open_route_service is not None

def test_get_location_coordinates_amstetten_stadtwerke(open_route_service):
    coordinates = open_route_service.get_location_coordinates("Stadtwerkestr. 2 Amstetten 3300 AT")
    assert coordinates is not None
    
    # Stadtwerkestr. 2 Amstetten 3300 AT
    expected_lon = 14.866910135695726
    expected_lat = 48.11370424217792
    
    assert abs(coordinates[0] - expected_lon) < 0.01 # longitude
    assert abs(coordinates[1] - expected_lat) < 0.01 # latitude

def test_get_location_coordinates_amstetten_mitterfeldstrasse(open_route_service):
    coordinates = open_route_service.get_location_coordinates("Mitterfeldstraße 7, Amstetten, None 3300 AT")
    assert coordinates is not None
    
    # Mitterfeldstraße 7, Amstetten, None 3300 AT
    expected_lon = 14.891356939571969
    expected_lat = 48.12452351273868
    
    assert abs(coordinates[0] - expected_lon) < 0.01 # longitude
    assert abs(coordinates[1] - expected_lat) < 0.01 # latitude

def test_get_location_coordinates_many_matching_locations(open_route_service):
    coordinates = open_route_service.get_location_coordinates("Industriepark Strasse A-8, 39245 Gommern, DE - ")
    
    # Industriepark Strasse A-9, 39245 Gommern, DE
    expected_lon = 11.816256055912472
    expected_lat = 52.08276960358608
    
    assert abs(coordinates[0] - expected_lon) < 0.01 # longitude
    assert abs(coordinates[1] - expected_lat) < 0.01 # latitude

@patch("openrouteservice.Client.pelias_search")
@patch("eco_tracker.api_cache.cached_api_call")
def test_get_location_coordinates_low_confidence(mock_cached_api_call, mock_pelias_search, open_route_service):
    mock_cached_api_call.return_value = None
    mock_pelias_search.return_value = {
        "features": [
            {"properties": {"confidence": 0.5}},
            {"properties": {"confidence": 0.6}}
        ]
    }
    
    with pytest.raises(exceptions.CoordinatesNotFound):
        open_route_service.get_location_coordinates("Industriepark Strasse A-9, 39245 Gommern, DE - saved in cache")

def test_get_location_coordinates_invalid_address(open_route_service):
    with pytest.raises(exceptions.ManyMatchingCoordinatesFound):
        open_route_service.get_location_coordinates("NAME OF A BUSINESS Fake street 2, not existent, 1234 something")


def test_get_route_distance(open_route_service):
    start, end = [14.891724, 48.123624], [14.866343, 48.112375]
    assert open_route_service.get_route_distance(start, end) is not None

def test_get_route_distance_invalid_coordinates(open_route_service):
    with pytest.raises(exceptions.RouteDistanceFailed):
        start, end = [0,0], [0,0]
        open_route_service.get_route_distance(start, end)

def test_get_distance_from_delivery_address(open_route_service):
    distance = open_route_service.get_distance_from_delivery_address("Stadtwerkestr. 2 Amstetten 3300 AT", "Mitterfeldstraße 7, Amstetten, 3300 AT")
    expected_distance = 3.9
    
    assert distance is not None
    assert abs(distance - expected_distance) < 0.1

def test_get_distance_from_delivery_address_longer_distance(open_route_service):
    distance = open_route_service.get_distance_from_delivery_address("Stadtwerkestr. 2 Amstetten 3300 AT", "Favoritenstraße 226, 1100 Wien")
    expected_distance = 134.0
    
    assert distance is not None
    assert abs(distance - expected_distance) < 5

def test_get_distance_from_delivery_address_invalid_address(open_route_service):
    with pytest.raises(exceptions.ManyMatchingCoordinatesFound):
        open_route_service.get_distance_from_delivery_address("Stadtwerkestr. 2 Amstetten 3300 AT", "NAME OF A BUSINESS Fake street 2, random city, 1234 country")
        
