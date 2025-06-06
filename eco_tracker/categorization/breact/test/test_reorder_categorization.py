from datetime import date
from unittest.mock import MagicMock

import pytest

from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer
from eco_tracker.categorization.breact.breact_reorder_categorization_filter import CategoryReorderFilter
from eco_tracker.product import Address, FailedSteps, Product


@pytest.fixture
def mock_breact_categorizer():
    mock = MagicMock(spec=BreactCategorizer)

    def generate_confidences(description, allowed_classes=None):
        # Simulate filtering based on allowed_classes
        all_confidences = {
            "Elektronik": 0.9,
            "Beleuchtung": 0.6,
            "Haushaltsgeraete": 0.8,
            "Service": 0.3,
        }
        if allowed_classes is None:
            return all_confidences
        return {k: v for k, v in all_confidences.items() if k in allowed_classes}

    mock.generate_confidences.side_effect = generate_confidences
    return mock


def test_category_reorder_step_reorders_by_confidence(mock_breact_categorizer):
    product = Product(
        delivered_date=date.today(),
        description="Smart LED lamp",
        unit="unit",
        quantity=1,
        unit_price=19.99,
        supplier="Test Supplier",
        supplier_address=Address("Test Street", "Test City", "12345", "Test Country"),
        delivery_address=Address("Test Street", "Test City", "12345", "Test Country"),
        delivery_transportation_type=None,
        delivery_emission_factor=None,
        estimated_categories=["Beleuchtung", "Elektronik", "Haushaltsgeraete", "Service"],
        estimated_matched_category="",
        category="",
        emission_factor=None,
        delivery_distance=0.0,
        weight=0.0,
        co2_purchase=0.0,
        co2_transport=0.0,
        failed_steps=FailedSteps(
            emission_factor_fetching=False,
            purchase_co2_calculation=False,
            estimate_categories=False,
            distance_estimation=False,
            weight_estimation=False,
            delivery_emissions_estimation=False
        )
    )

    next_step = MagicMock()  # fake a call to check later
    reorder_step = CategoryReorderFilter(mock_breact_categorizer)

    reorder_step(product, next_step)

    # Check if categories were filtered by confidence threshold (>=0.7) and sorted descending
    # "Beleuchtung" and "Service" should be excluded due to confidence < 0.7
    assert product.estimated_categories == ["Elektronik", "Haushaltsgeraete"]

    # check if pipeline continues
    next_step.assert_called_once_with(product)

    # check that the new generate_confidences was called and not the old get_confidence_for_class
    mock_breact_categorizer.generate_confidences.assert_called_once_with(
        product.description,
        ["Beleuchtung", "Elektronik", "Haushaltsgeraete", "Service"]
    )
