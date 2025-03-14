import os

import pytest
from dotenv import load_dotenv

import eco_tracker.categorization.climatiq_categorization as categorization


@pytest.fixture
def api_key() -> str:
    load_dotenv()
    return os.getenv("LLM_API_KEY")

@pytest.fixture
def llm_client(api_key) -> categorization.ClimatiqCategorization:
    return categorization.ClimatiqCategorization(llm_api_key=api_key)

def test_generate_categorization_success(llm_client):
    num_of_categories = 15
    categories = llm_client.generate_categorization(product="Liebherr FreshAir Aktivkohlefilter  9096989-00", num_of_categories=num_of_categories)
    assert categories is not None
    assert isinstance(categories, list)
    assert len(categories) == num_of_categories
    for category in categories:
        assert isinstance(category, str)
        assert 1 <= len(category.split(" ")) <= 3
