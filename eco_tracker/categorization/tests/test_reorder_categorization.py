import pytest
from unittest.mock import MagicMock

from eco_tracker.product import Product
from eco_tracker.categorization.breact_categorization import BreactCategorizer
from eco_tracker.pipeline import NextStep
from eco_tracker.categorization.reorder_categorization import CategoryReorderStep


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
        description="Smart LED lamp",
        unit="unit",
        quantity=1,
        price=19.99,
        status="",
        climatiq_categories=["Beleuchtung", "Elektronik", "Haushaltsgeraete", "Service"],
        category="",
        emission_factor=None,
        co2e=0,
    )

    next_step = MagicMock()  # fake a call to check later
    reorder_step = CategoryReorderStep(mock_breact_categorizer)

    reorder_step(product, next_step)

    # Check if categories were sorted by confidence (Elektronik > Haushaltsgeraete > Beleuchtung > Service)
    assert product.climatiq_categories == ["Elektronik", "Haushaltsgeraete", "Beleuchtung", "Service"]

    # check if pipeline continues
    next_step.assert_called_once_with(product)
