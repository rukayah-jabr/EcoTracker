import os

import pytest
from dotenv import load_dotenv

from eco_tracker.categorization.climatiq_categorization import ClimatiqCategorizer
from eco_tracker.categorization.climatiq_categorization_filter import ClimatiqCategorizerFilter
from eco_tracker.product import Product
from eco_tracker.emission_factors.climatiq import Climatiq
from eco_tracker.emission_factors.emission_factors_filter import EmissionFactorsFilter
from eco_tracker.pipeline import Pipeline


@pytest.fixture
def climatiq():
		load_dotenv()
		return Climatiq(os.getenv("CLIMATIQ_API_KEY"))

@pytest.fixture
def categorizer():
	load_dotenv()
	return ClimatiqCategorizer(os.getenv("LLM_API_KEY"))

@pytest.fixture
def emission_factors_filter(climatiq):
	return EmissionFactorsFilter(climatiq, "^20")

@pytest.fixture
def climatiq_categorizer(categorizer):
	return ClimatiqCategorizerFilter(categorizer)

@pytest.fixture
def product():
	return Product(
		description="Lenovo Yoga 15",
		unit="unit",
		quantity=1,
		price=1000,
		status="status",
		climatiq_categories=[],
		category="category",
		emission_factor=None,
		co2e=0,
	)

def test_fetch_emission_factor(emission_factors_filter, climatiq_categorizer, product):
	pipeline = Pipeline[Product](
		climatiq_categorizer,
		emission_factors_filter,
	)

	pipeline(product)

	assert product.climatiq_categories is not None
	assert product.emission_factor.co2e is not None
	assert product.emission_factor.co2e_unit is not None
	assert product.emission_factor.activity_unit is not None
