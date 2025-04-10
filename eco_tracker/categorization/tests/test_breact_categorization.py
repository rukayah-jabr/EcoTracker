import os
import pytest
from dotenv import load_dotenv

from eco_tracker.categorization.breact_categorization import BreactCategorizer


@pytest.fixture
def breact_api_key() -> str:
    load_dotenv()
    return os.getenv("BREACT_API_KEY")


@pytest.fixture
def breact_client(breact_api_key) -> BreactCategorizer:
    return BreactCategorizer(breact_api_key=breact_api_key)


def test_breact_generate_categorization_success(breact_client):
    product = "Delonghi espresso machine stainless steel"
    categories = breact_client.generate_categorization(product=product)

    assert categories is not None
    assert isinstance(categories, list) #still need to be checked if its really a list in case of single class
    assert len(categories) == 1 #single class
    assert isinstance(categories[0], str) #checks if the content is string
    assert len(categories[0]) > 0 #empty string
