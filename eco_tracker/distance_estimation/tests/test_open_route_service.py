import pytest
import os
import openrouteservice
from dotenv import load_dotenv
from eco_tracker.distance_estimation import exceptions
from eco_tracker.distance_estimation.open_route_service import get_location_coordinates, get_route_distance


def test_openrouteservice_instance():
    load_dotenv()
    API_KEY = os.getenv("OPEN_ROUTE_SERVICE_API_KEY")
    client = openrouteservice.Client(key=API_KEY)
    assert client is not None

def test_get_location_coordinates():
    assert get_location_coordinates("Mitterfeldstraße 7, Amstetten, None 3300 AT") is not None
    assert get_location_coordinates("Stadtwerkestr. 2 Amstetten 3300 AT") is not None

    with pytest.raises(exceptions.CoordinatesNotFound):
        get_location_coordinates("NAME OF A BUSINESS Fake street 2, random city, 1234 country")

def test_get_route_distance():
    start, end = [14.891724, 48.123624], [14.866343, 48.112375]
    assert get_route_distance(start, end) is not None

    with pytest.raises(exceptions.RouteDistanceFailed):
        start, end = [0,0], [0,0]
        get_route_distance(start, end)