import pytest
from datetime import date
from eco_tracker.categorization.breact.breact_fe_categorization_filter import BreactFrontendCategorizationFilter
from eco_tracker.product import Address, FailedSteps, Product

class MockBreactCategorizer:
    def generate_categorization(self, description, num_of_categories=10):
        return ["Kaffee & Zubehoer"]

class FailingMockBreactCategorizer:
    def generate_categorization(self, description, num_of_categories=10):
        raise Exception("API error")

def create_test_product() -> Product:
        return Product(
        delivered_date=date.today(),
        description="Espresso machine",
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

def test_breact_fe_categorization_assigns_category():
    mock_categorizer = MockBreactCategorizer()
    filter_step = BreactFrontendCategorizationFilter(mock_categorizer)
    product = create_test_product()


    def dummy_next_step(p): pass

    filter_step(product, dummy_next_step)

    assert product.category == "Kaffee & Zubehoer"

def test_breact_fe_categorization_fallback_on_exception():
    mock_categorizer = FailingMockBreactCategorizer()
    filter_step = BreactFrontendCategorizationFilter(mock_categorizer)
    product = create_test_product()

    def dummy_next_step(p): pass

    filter_step(product, dummy_next_step)

    assert product.category == "others"