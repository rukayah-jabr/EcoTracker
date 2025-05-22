import os
from datetime import date
from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv

from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer
from eco_tracker.categorization.breact.breact_reorder_categorization import CategoryReorderStep
from eco_tracker.categorization.climatiq_categorization_filter import ClimatiqCategorizerFilter
from eco_tracker.categorization.groq.groq_categorizer import ClimatiqCategorizer
from eco_tracker.distance_estimation.distance_estimation_filter import DistanceEstimationFilter
from eco_tracker.distance_estimation.open_route_service.open_route_service import OpenRouteService
from eco_tracker.emission_factors.climatiq.climatiq import Climatiq
from eco_tracker.emission_factors.emission_factors_filter import EmissionFactorsFilter
from eco_tracker.pipeline import Pipeline
from eco_tracker.product import Address, FailedSteps, Product
from eco_tracker.purchase_emissions.basic_estimator.basic_estimator import BasicPurchaseEmissionsEstimator
from eco_tracker.purchase_emissions.purchase_estimator_filter import PurchaseEmissionsEstimatorFilter


@pytest.fixture
def climatiq():
		load_dotenv()
		api_key = os.getenv("CLIMATIQ_API_KEY")
		if not api_key:
			raise ValueError("CLIMATIQ_API_KEY is not set")
		return Climatiq(api_key)

@pytest.fixture
def categorizer():
	load_dotenv()
	llm_api_key = os.getenv("LLM_API_KEY")
	if not llm_api_key:
		raise ValueError("LLM_API_KEY is not set")
	return ClimatiqCategorizer(llm_api_key)

@pytest.fixture
def breact_categorizer():
    mock = MagicMock()
    mock.get_confidence_for_class.return_value = 1.0
    return mock

@pytest.fixture
def open_route_service():
	load_dotenv()
	open_route_service_api_key = os.getenv("OPEN_ROUTE_SERVICE_API_KEY")
	if not open_route_service_api_key:
		raise ValueError("OPEN_ROUTE_SERVICE_API_KEY is not set")
	return OpenRouteService(open_route_service_api_key)

@pytest.fixture
def purchase_emissions_estimator():
	return BasicPurchaseEmissionsEstimator()

@pytest.fixture
def emission_factors_filter(climatiq, breact_categorizer) -> EmissionFactorsFilter:
	return EmissionFactorsFilter(climatiq, "^21", breact_categorizer)

@pytest.fixture
def climatiq_categorizer_filter(categorizer) -> ClimatiqCategorizerFilter:
	return ClimatiqCategorizerFilter(categorizer)

@pytest.fixture
def category_reorder_step(breact_categorizer) -> CategoryReorderStep:
	return CategoryReorderStep(breact_categorizer)

@pytest.fixture
def purchase_emissions_estimator_filter(purchase_emissions_estimator) -> PurchaseEmissionsEstimatorFilter:
	return PurchaseEmissionsEstimatorFilter(purchase_emissions_estimator)

@pytest.fixture
def distance_estimation_filter(open_route_service) -> DistanceEstimationFilter:
	return DistanceEstimationFilter(open_route_service)

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
		emission_factor=None,
		delivery_emission_factor=None,
		delivery_distance=0,
		weight=0,
		co2_purchase=0,
		co2_transport=0,
		failed_steps=FailedSteps(
			estimate_categories=False,
			emission_factor_fetching=False,
			purchase_co2_calculation=False,
			distance_estimation=False,
			weight_estimation=False,
			delivery_emissions_estimation=False
		)
	)

def test_estimate_category_1_emissions(emission_factors_filter, category_reorder_step, climatiq_categorizer_filter, purchase_emissions_estimator_filter, distance_estimation_filter, product):
	pipeline = Pipeline[Product](
		climatiq_categorizer_filter,
		category_reorder_step,
		emission_factors_filter,
		purchase_emissions_estimator_filter
	)

	pipeline(product)

	assert product.climatiq_categories is not None
	assert product.emission_factor.co2e is not None
	assert product.emission_factor.co2e_unit is not None
	assert product.emission_factor.activity_unit is not None
	assert product.co2_purchase is not None
