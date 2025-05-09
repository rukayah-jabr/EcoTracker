

from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from eco_tracker.emission_factors.emission_factors_filter import EmissionFactorsFilter
from eco_tracker.emission_factors.emission_factors_interface import EmissionFactor
from eco_tracker.emission_factors.exceptions import EmissionFactorNotFound
from eco_tracker.product import Address, FailedSteps, Product


@pytest.fixture
def product():
  return Product(
    description="test",
    unit="test",
    quantity=1,
    unit_price=1,
      supplier="test",
      supplier_address=Address(
        "test",
        "test",
        "test",
        "test"
      ),
      delivery_address=Address(
        "test",
        "test",
        "test",
        "test"
      ),
      climatiq_categories=["test"],
      climatiq_matched_category=None,
      category="test",
      emission_factor=None,
      delivery_emission_factor=None,
      delivery_distance=0,
      delivery_transportation_type=None,
      weight=0,
      delivered_date=date(2021, 1, 1),
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

@pytest.fixture
def emission_factor():
  return EmissionFactor(co2e=1, co2e_unit="kg", activity_unit="l", name="test", description="test")

def test_emission_factors_filter_estimate_categories_failed(product):
  product.failed_steps.estimate_categories = True
  emission_factors_filter = EmissionFactorsFilter(MagicMock(), "^21")
  emission_factors_filter(product, lambda x: None)
  assert product.failed_steps.emission_factor_fetching == True

def test_emission_factors_filter_emission_factor_not_found(product):
  mock_emission_factors_fetcher = MagicMock()
  mock_emission_factors_fetcher.fetch_emission_factor_from_query.side_effect = EmissionFactorNotFound("test")
  emission_factors_filter = EmissionFactorsFilter(mock_emission_factors_fetcher, "^21")
  emission_factors_filter(product, lambda x: None)
  assert product.failed_steps.emission_factor_fetching == True

def test_emission_factors_filter_emission_factor_unexpected_error(product):
  mock_emission_factors_fetcher = MagicMock()
  mock_emission_factors_fetcher.fetch_emission_factor_from_query.side_effect = Exception("test")
  emission_factors_filter = EmissionFactorsFilter(mock_emission_factors_fetcher, "^21")
  with pytest.raises(Exception):
    emission_factors_filter(product, lambda x: None)

def test_emission_factors_filter_emission_factor_found(product, emission_factor):
  mock_emission_factors_fetcher = MagicMock()
  mock_emission_factors_fetcher.fetch_emission_factor_from_query.return_value = emission_factor
  emission_factors_filter = EmissionFactorsFilter(mock_emission_factors_fetcher, "^21")
  emission_factors_filter(product, lambda x: None)
  assert product.emission_factor == emission_factor
