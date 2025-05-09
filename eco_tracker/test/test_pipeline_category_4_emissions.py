import os
from datetime import date

import pytest
from delivery_emissions.delivery_emissions_estimator_filter import DeliveryEmissionsEstimatorFilter
from dotenv import load_dotenv

from eco_tracker.delivery_emissions.distance_based_method.distance_based_method import DistanceBasedMethod
from eco_tracker.distance_estimation.distance_estimation_filter import DistanceEstimationFilter
from eco_tracker.distance_estimation.open_route_service.open_route_service import OpenRouteService
from eco_tracker.emission_factors_transportation.basic_impl.basic_impl import BasicEmissionFactorsTransportationFetcher
from eco_tracker.emission_factors_transportation.emission_factors_transportation_filter import EmissionFactorsTransportationFilter
from eco_tracker.pipeline import Pipeline
from eco_tracker.product import Address, FailedSteps, Product
from eco_tracker.weight_estimation.groq.groq import GroqWeightEstimator
from eco_tracker.weight_estimation.weight_estimation_filter import WeightEstimationFilter


@pytest.fixture
def open_route_service():
	load_dotenv()
	open_route_service_api_key = os.getenv("OPEN_ROUTE_SERVICE_API_KEY")
	if not open_route_service_api_key:
		raise ValueError("OPEN_ROUTE_SERVICE_API_KEY is not set")
	return OpenRouteService(open_route_service_api_key)

@pytest.fixture
def emission_factors_transportation_fetcher():
	return BasicEmissionFactorsTransportationFetcher()

@pytest.fixture
def groq_weight_estimator():
	load_dotenv()
	groq_api_key = os.getenv("LLM_API_KEY")
	if not groq_api_key:
		raise ValueError("LLM_API_KEY is not set")
	return GroqWeightEstimator(groq_api_key)

@pytest.fixture
def distance_based_method():
	return DistanceBasedMethod()

@pytest.fixture
def distance_estimation_filter(open_route_service) -> DistanceEstimationFilter:
	return DistanceEstimationFilter(open_route_service)

@pytest.fixture
def emission_factors_transportation_filter(emission_factors_transportation_fetcher) -> EmissionFactorsTransportationFilter:
	return EmissionFactorsTransportationFilter(emission_factors_transportation_fetcher)

@pytest.fixture
def weight_estimation_filter(groq_weight_estimator) -> WeightEstimationFilter:
	return WeightEstimationFilter(groq_weight_estimator)

@pytest.fixture
def delivery_emissions_estimator_filter(distance_based_method) -> DeliveryEmissionsEstimatorFilter:
	return DeliveryEmissionsEstimatorFilter(distance_based_method)

@pytest.fixture
def product():
	return Product(
		delivered_date=date(2024, 1, 1),
		description="Lenovo Yoga 15",
		unit="number",
		unit_price=1000.00,
		quantity=2,
		climatiq_categories=[],
		climatiq_matched_category=None,
		category="category",
		supplier="supplier",
		supplier_address= Address(
			street="Schönbrunnerstraße 1",
			city="Vienna",
			zip="1010",
			country="AT"
		),
		delivery_address= Address(
			street="Stadtwerkestr. 2",
			city="Amstetten",
			zip="3300",
			country="AT"
		),
		delivery_transportation_type=None,
  	weight=0,
		emission_factor=None,
		delivery_emission_factor=None,
		delivery_distance=0,
		co2_purchase=0,
		co2_transport=0,
		failed_steps=FailedSteps(
			estimate_categories=False,
			emission_factor_fetching=False,
			purchase_co2_calculation=False,
			distance_estimation=False,
			weight_estimation=False,
			delivery_emissions_estimation=False
		),
	)
 
def test_estimate_category_4_emissions(distance_estimation_filter, emission_factors_transportation_filter, weight_estimation_filter, delivery_emissions_estimator_filter, product):
	pipeline = Pipeline[Product](
		distance_estimation_filter,
		emission_factors_transportation_filter,
		weight_estimation_filter,
		delivery_emissions_estimator_filter
	)

	pipeline(product)

	assert product.delivery_distance is not None
	assert product.delivery_emission_factor is not None
	assert product.weight is not None
	assert product.co2_transport != 0
	# assert product.co2_transport is not None
