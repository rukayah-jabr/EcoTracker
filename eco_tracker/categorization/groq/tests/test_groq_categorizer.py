import os
from unittest.mock import Mock, patch

import pytest
import requests
from dotenv import load_dotenv

import eco_tracker.categorization.groq.groq_categorizer as categorization
from eco_tracker import exceptions


@pytest.fixture
def api_key() -> str:
    load_dotenv()
    llm_api_key = os.getenv("LLM_API_KEY")
    assert llm_api_key is not None, "LLM_API_KEY is not set"
    return llm_api_key

@pytest.fixture
def llm_client(api_key) -> categorization.ClimatiqCategorizer:
    return categorization.ClimatiqCategorizer(llm_api_key=api_key)

def test_generate_categorization_success(llm_client):
    num_of_categories = 15
    categories = llm_client.generate_categorization(product="Liebherr FreshAir Aktivkohlefilter  9096989-00", num_of_categories=num_of_categories)
    assert categories is not None
    assert isinstance(categories, list)
    assert len(categories) == num_of_categories
    for category in categories:
        assert isinstance(category, str)
        assert 1 <= len(category.split(" ")) <= 3


@patch('requests.post')
@patch('eco_tracker.api_cache.cached_api_call')
def test_generate_categorization_http_error(mock_cached_api_call, mock_post, llm_client):
    mock_cached_api_call.return_value = None
    
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Server Error"
    mock_post.return_value = mock_response
    
    with pytest.raises(exceptions.HTTPException) as exc_info:
        llm_client.generate_categorization(product="TestProduct", num_of_categories=15)
    
    assert exc_info.value.status_code == 500
