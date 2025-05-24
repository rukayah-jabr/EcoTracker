

from datetime import date
from unittest.mock import MagicMock, patch

import pytest
import logging

from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer
from eco_tracker.emission_factors.emission_factors_filter import EmissionFactorsFilter
from eco_tracker.emission_factors.emission_factors_interface import EmissionFactor
from eco_tracker.emission_factors.exceptions import EmissionFactorNotFound
from eco_tracker.product import Address, FailedSteps, Product
from eco_tracker.test.test_pipeline_category_1_emissions import breact_categorizer


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
      estimated_categories=["test"],
      estimated_matched_category=None,
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

@pytest.fixture
def breact_categorizer():
    mock = MagicMock()
    mock.get_confidence_for_class.return_value = 1.0
    return mock

def test_emission_factors_filter_estimate_categories_failed(product, breact_categorizer):
  product.failed_steps.estimate_categories = True
  emission_factors_filter = EmissionFactorsFilter(MagicMock(), "^21", breact_categorizer)
  emission_factors_filter(product, lambda x: None)
  assert product.failed_steps.emission_factor_fetching == True

def test_emission_factors_filter_emission_factor_not_found(product, breact_categorizer):
  mock_emission_factors_fetcher = MagicMock()
  mock_emission_factors_fetcher.fetch_emission_factor_from_query.side_effect = EmissionFactorNotFound("test")
  emission_factors_filter = EmissionFactorsFilter(mock_emission_factors_fetcher, "^21", breact_categorizer)
  emission_factors_filter(product, lambda x: None)
  assert product.failed_steps.emission_factor_fetching == True

def test_emission_factors_filter_emission_factor_unexpected_error(product, breact_categorizer):
  mock_emission_factors_fetcher = MagicMock()
  mock_emission_factors_fetcher.fetch_emission_factor_from_query.side_effect = Exception("test")
  emission_factors_filter = EmissionFactorsFilter(mock_emission_factors_fetcher, "^21", breact_categorizer)
  with pytest.raises(Exception):
    emission_factors_filter(product, lambda x: None)

def test_emission_factors_filter_emission_factor_found(product, emission_factor, breact_categorizer):
  mock_emission_factors_fetcher = MagicMock()
  mock_emission_factors_fetcher.fetch_emission_factor_from_query.return_value = emission_factor
  emission_factors_filter = EmissionFactorsFilter(mock_emission_factors_fetcher, "^21", breact_categorizer)
  emission_factors_filter(product, lambda x: None)
  assert product.emission_factor == emission_factor


def test_emission_factors_filter_low_confidence_skips_category(product, emission_factor, breact_categorizer):
    # low confidence so emission factor fetching is skipped
    breact_categorizer.get_confidence_for_class.return_value = 0.5
    mock_emission_factors_fetcher = MagicMock()
    mock_emission_factors_fetcher.fetch_emission_factor_from_query.return_value = emission_factor

    emission_factors_filter = EmissionFactorsFilter(mock_emission_factors_fetcher, "^21", breact_categorizer)
    emission_factors_filter(product, lambda x: None)

    # emission_factor should NOT be set
    assert product.emission_factor is None


def test_emission_factors_filter_no_suitable_emission_factor_logs_error_and_sets_failed(product, breact_categorizer, caplog):
  # Setup categorizer to return high confidence but fetcher always raises EmissionFactorNotFound
  breact_categorizer.get_confidence_for_class.return_value = 1.0
  mock_emission_factors_fetcher = MagicMock()
  mock_emission_factors_fetcher.fetch_emission_factor_from_query.side_effect = EmissionFactorNotFound("No factor")

  emission_factors_filter = EmissionFactorsFilter(mock_emission_factors_fetcher, "^21", breact_categorizer)

  with caplog.at_level(logging.ERROR):
    emission_factors_filter(product, lambda x: None)

  # failed_steps.emission_factor_fetching should be True after no matches
  assert product.failed_steps.emission_factor_fetching is True

  # Log message about no suitable emission factor found should appear
  found_log = any("No suitable emission factor found" in record.message for record in caplog.records)
  assert found_log