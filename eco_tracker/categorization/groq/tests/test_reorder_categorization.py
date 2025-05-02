from datetime import date
from unittest.mock import MagicMock

import pytest

from eco_tracker.categorization.breact_categorization import BreactCategorizer
from eco_tracker.categorization.reorder_categorization import CategoryReorderStep
from eco_tracker.pipeline import NextStep
from eco_tracker.product import Product, SupplierAddress


@pytest.fixture
def mock_breact_categorizer():
    mock = MagicMock(spec=BreactCategorizer)
    # Simulated confidence values per category
    mock.get_confidence_for_class.side_effect = lambda desc, cat: {
        "Elektronik": 0.9,
        "Beleuchtung": 0.6,
        "Haushaltsgeraete": 0.8
    }.get(cat, 0.0)
    return mock


def test_category_reorder_step_reorders_by_confidence(mock_breact_categorizer):
    product = Product(
        delivered_date=date.today(),
        description="Smart LED lamp",
        unit="unit",
        quantity=1,
        unit_price=19.99,
        supplier="Test Supplier",
        supplier_address=SupplierAddress("Test Street", "Test City", "Test State", "12345", "Test Country"),
        climatiq_categories=["Beleuchtung", "Elektronik", "Haushaltsgeraete", "Service"],
        climatiq_matched_category="",
        category="",
        emission_factor=None,
        delivery_distance=0.0,
        co2_purchase=0.0,
        co2_transport=0.0,
    )

    next_step = MagicMock()  # fake a call to check later
    reorder_step = CategoryReorderStep(mock_breact_categorizer)

    reorder_step(product, next_step)

    # Check if categories were sorted by confidence and categories below the threshold were discarded (Elektronik > Haushaltsgeraete), Beleuchtung and Service should be ignored
    assert product.climatiq_categories == ["Elektronik", "Haushaltsgeraete"]

    # check if pipeline continues
    next_step.assert_called_once_with(product)
