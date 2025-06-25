import pytest
from unittest.mock import patch
from geopy.distance import geodesic

from eco_tracker.distance_estimation.open_route_service.open_route_service import OpenRouteService
from eco_tracker.distance_estimation import exceptions

API_KEY = "dummy_key"

class TestOpenRouteService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.ors = OpenRouteService(api_key=API_KEY)

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.api_cache.execute_or_get_from_cache')
    def test_get_route_distance_success(self, mock_cache):
        # make decorator a no-op
        mock_cache.side_effect = lambda *args, **kwargs: lambda f: f
        with patch.object(self.ors.client, 'directions', return_value={
            'features': [{'properties': {'segments': [{'distance': 12345}]}}]
        }):
            dist = self.ors.get_route_distance((1.0, 2.0), (3.0, 4.0))
            assert dist == pytest.approx(12.345)

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.api_cache.execute_or_get_from_cache')
    def test_get_route_distance_failure(self, mock_cache):
        mock_cache.side_effect = lambda *args, **kwargs: lambda f: f
        with patch.object(self.ors.client, 'directions', side_effect=Exception("API failure")):
            with pytest.raises(exceptions.RouteDistanceFailed):
                self.ors.get_route_distance((1.0, 2.0), (3.0, 4.0))

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.api_cache.execute_or_get_from_cache')
    def test_get_location_coordinates_success(self, mock_cache):
        mock_cache.side_effect = lambda *args, **kwargs: lambda f: f
        mock_geojson = {
            "features": [
                {"properties": {"confidence": 0.8}, "geometry": {"coordinates": (10.0, 20.0)}}
            ]
        }
        with patch.object(self.ors.client, 'pelias_search', return_value=mock_geojson):
            coords = self.ors.get_location_coordinates("valid address")
            assert coords == (10.0, 20.0)

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.api_cache.execute_or_get_from_cache')
    def test_get_location_coordinates_no_features(self, mock_cache):
        mock_cache.side_effect = lambda *args, **kwargs: lambda f: f
        with patch.object(self.ors.client, 'pelias_search', return_value={"features": []}):
            with pytest.raises(exceptions.CoordinatesNotFound):
                self.ors.get_location_coordinates("no features")

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.api_cache.execute_or_get_from_cache')
    def test_get_location_coordinates_low_confidence_skips(self, mock_cache):
        mock_cache.side_effect = lambda *args, **kwargs: lambda f: f
        mock_geojson = {
            "features": [
                {"properties": {"confidence": 0.6}, "geometry": {"coordinates": (10.0, 20.0)}}
            ]
        }
        with patch.object(self.ors.client, 'pelias_search', return_value=mock_geojson):
            with pytest.raises(exceptions.CoordinatesNotFound):
                self.ors.get_location_coordinates("low confidence")

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.api_cache.execute_or_get_from_cache')
    def test_get_location_coordinates_many_matching_coordinates(self, mock_cache):
        mock_cache.side_effect = lambda *args, **kwargs: lambda f: f
        mock_geojson = {
            "features": [
                {"properties": {"confidence": 0.8}, "geometry": {"coordinates": (10.0, 20.0)}},
                {"properties": {"confidence": 0.9}, "geometry": {"coordinates": (100.0, 200.0)}},
            ]
        }
        with patch.object(self.ors.client, 'pelias_search', return_value=mock_geojson), \
             patch.object(self.ors, 'get_distance_between_coordinates', return_value=11):
            with pytest.raises(exceptions.ManyMatchingCoordinatesFound):
                self.ors.get_location_coordinates("multiple far matches")

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.api_cache.execute_or_get_from_cache')
    def test_get_location_coordinates_api_exception(self, mock_cache):
        mock_cache.side_effect = lambda *args, **kwargs: lambda f: f
        with patch.object(self.ors.client, 'pelias_search', side_effect=Exception("API error")):
            with pytest.raises(exceptions.CoordinatesNotFound):
                self.ors.get_location_coordinates("api error")

    def test_get_distance_between_coordinates(self):
        start = (50.0, 5.0)
        end = (51.0, 6.0)
        expected_distance = geodesic((5.0, 50.0), (6.0, 51.0)).km
        dist = self.ors.get_distance_between_coordinates(start, end)
        assert dist == pytest.approx(expected_distance)

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.OpenRouteService.get_location_coordinates')
    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.OpenRouteService.get_route_distance')
    def test_get_distance_from_delivery_address_success(self, mock_route_dist, mock_loc_coords):
        mock_loc_coords.side_effect = [(10.0, 20.0), (11.0, 21.0)]
        mock_route_dist.return_value = 5.0
        dist = self.ors.get_distance_from_delivery_address("supplier", "delivery")
        assert dist == 5.0

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.OpenRouteService.get_location_coordinates')
    def test_get_distance_from_delivery_address_same_coordinates(self, mock_loc_coords):
        mock_loc_coords.side_effect = [(10.0, 20.0), (10.0, 20.0)]
        dist = self.ors.get_distance_from_delivery_address("supplier", "delivery")
        assert dist == 0

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.OpenRouteService.get_location_coordinates')
    def test_get_distance_from_delivery_address_coordinates_not_found(self, mock_loc_coords):
        mock_loc_coords.side_effect = exceptions.CoordinatesNotFound("addr")
        with pytest.raises(exceptions.CoordinatesNotFound):
            self.ors.get_distance_from_delivery_address("supplier", "delivery")

    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.OpenRouteService.get_location_coordinates')
    @patch('eco_tracker.distance_estimation.open_route_service.open_route_service.OpenRouteService.get_route_distance')
    def test_get_distance_from_delivery_address_route_distance_failed(self, mock_route_dist, mock_loc_coords):
        mock_loc_coords.side_effect = [(10.0, 20.0), (11.0, 21.0)]
        mock_route_dist.return_value = None
        with pytest.raises(exceptions.RouteDistanceFailed):
            self.ors.get_distance_from_delivery_address("supplier", "delivery")
