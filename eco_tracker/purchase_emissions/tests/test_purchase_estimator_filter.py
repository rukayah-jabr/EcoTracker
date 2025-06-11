from datetime import date
from unittest.mock import MagicMock

import pytest

from eco_tracker.product import Address, EmissionFactor, FailedSteps, Product
from eco_tracker.purchase_emissions.purchase_estimator_filter import PurchaseEmissionsEstimatorFilter


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
      emission_factor=EmissionFactor(co2e=1, co2e_unit="kg", activity_unit="l", name="test", description="test"),
      delivery_emission_factor=None,
      delivery_distance=0,
      weight=0,
      delivery_transportation_type=None,
      delivery=None,
      delivered_date=date(2021, 1, 1),
      co2_purchase=0,
      co2_transport=0,
      failed_steps=FailedSteps(
        estimate_categories=False,
        reorder_categories=False,
        emission_factor_fetching=False,
        purchase_co2_calculation=False,
        distance_estimation=False,
        weight_estimation=False,
        delivery_emissions_estimation=False
      ),
      min_emission_factor_confidence=0.7
    )

def test_purchase_estimator_filter_emission_factor_fetching_failed(product):
    product.failed_steps.emission_factor_fetching = True
    mock_estimator = MagicMock()
    
    next_step = MagicMock()
    
    purchase_estimator_filter = PurchaseEmissionsEstimatorFilter(mock_estimator)
    purchase_estimator_filter(product, next_step)
    
    assert product.failed_steps.purchase_co2_calculation == True
    assert mock_estimator.call_count == 0
    assert next_step.call_count == 1

def test_purchase_estimator_filter_estimate_emissions_failed(product):
    mock_estimator = MagicMock()
    mock_estimator.estimate_emissions.side_effect = Exception("test")
    
    next_step = MagicMock()
    
    purchase_estimator_filter = PurchaseEmissionsEstimatorFilter(mock_estimator)
    purchase_estimator_filter(product, next_step)
    
    assert mock_estimator.estimate_emissions.call_count == 1
    assert next_step.call_count == 1
      
      
def test_purchase_estimator_filter_estimate_emissions_success(product):
    mock_estimator = MagicMock()
    mock_estimator.estimate_emissions.return_value = 1
    
    next_step = MagicMock()
    
    purchase_estimator_filter = PurchaseEmissionsEstimatorFilter(mock_estimator)
    purchase_estimator_filter(product, next_step)
    
    assert mock_estimator.estimate_emissions.call_count == 1
    assert next_step.call_count == 1
    assert product.co2_purchase == 1