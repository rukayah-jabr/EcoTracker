from unittest.mock import Mock

import pytest

from eco_tracker.product import EmissionFactor, Product
from eco_tracker.purchase_emissions.basic_estimator.basic_estimator import BasicPurchaseEmissionsEstimator
from eco_tracker.purchase_emissions.exceptions import NotSupportedMeasurementUnit, PurchaseEmissionFactorNotSet


@pytest.fixture
def basic_estimator():
    return BasicPurchaseEmissionsEstimator()


@pytest.fixture
def product_with_no_emission_factor():
    product = Mock(spec=Product)
    product.emission_factor = None
    product.description = "Test Product"
    return product


@pytest.fixture
def product_with_empty_unit():
    product = Mock(spec=Product)
    emission_factor = Mock(spec=EmissionFactor)
    emission_factor.activity_unit = ""
    emission_factor.co2e = 10.0
    product.emission_factor = emission_factor
    product.quantity = 2.0
    return product


@pytest.fixture
def product_with_liter_unit():
    product = Mock(spec=Product)
    emission_factor = Mock(spec=EmissionFactor)
    emission_factor.activity_unit = "l"
    emission_factor.co2e = 5.0
    product.emission_factor = emission_factor
    product.quantity = 3.0
    return product


@pytest.fixture
def product_with_euro_unit():
    product = Mock(spec=Product)
    emission_factor = Mock(spec=EmissionFactor)
    emission_factor.activity_unit = "eur"
    emission_factor.co2e = 0.5
    product.emission_factor = emission_factor
    product.quantity = 4.0
    product.unit_price = 10.0
    return product


@pytest.fixture
def product_with_unsupported_unit():
    product = Mock(spec=Product)
    emission_factor = Mock(spec=EmissionFactor)
    emission_factor.activity_unit = "kg"
    product.emission_factor = emission_factor
    return product


def test_emission_factor_not_set(basic_estimator, product_with_no_emission_factor):
    with pytest.raises(PurchaseEmissionFactorNotSet) as exc_info:
        basic_estimator.estimate_emissions(product_with_no_emission_factor)
    
    assert product_with_no_emission_factor.description in str(exc_info.value)


def test_empty_unit_emission_calculation(basic_estimator, product_with_empty_unit):
    result = basic_estimator.estimate_emissions(product_with_empty_unit)
    
    # co2e * quantity
    expected = 10.0 * 2.0
    assert result == expected


def test_liter_unit_emission_calculation(basic_estimator, product_with_liter_unit):
    result = basic_estimator.estimate_emissions(product_with_liter_unit)
    
    # co2e * quantity
    expected = 5.0 * 3.0
    assert result == expected


def test_euro_unit_emission_calculation(basic_estimator, product_with_euro_unit):
    result = basic_estimator.estimate_emissions(product_with_euro_unit)
    
    # co2e * quantity * unit_price
    expected = 0.5 * 4.0 * 10.0
    assert result == expected


def test_unsupported_unit_raises_exception(basic_estimator, product_with_unsupported_unit):
    with pytest.raises(NotSupportedMeasurementUnit) as exc_info:
        basic_estimator.estimate_emissions(product_with_unsupported_unit)
    
    assert product_with_unsupported_unit.emission_factor.activity_unit in str(exc_info.value) 