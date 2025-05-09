import os

import pytest

from eco_tracker.weight_estimation.groq.groq import GroqWeightEstimator


@pytest.fixture
def groq_weight_estimator():
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        pytest.skip("LLM_API_KEY environment variable not set")
    return GroqWeightEstimator(api_key)

def test_estimate_weight_coffee_machine(groq_weight_estimator):
    product_description = "DeLonghi EN80B Inissia black AA20603"

    weight = groq_weight_estimator.estimate_weight(product_description)

    assert isinstance(weight, float)
    assert weight > 0

def test_estimate_weight_tv(groq_weight_estimator):
    product_description = "Samsung 43DU7190 Ultra HD HDR LED-TV 43 (108 cm)"

    weight = groq_weight_estimator.estimate_weight(product_description)

    assert isinstance(weight, float)
    assert weight > 0

def test_estimate_weight_of_quantity_tv(groq_weight_estimator):
    product_description = "Samsung 43DU7190 Ultra HD HDR LED-TV 43 (108 cm)"
    quantity = 2

    weight = groq_weight_estimator.estimate_weight_of_quantity(product_description, quantity)

    assert isinstance(weight, float)
