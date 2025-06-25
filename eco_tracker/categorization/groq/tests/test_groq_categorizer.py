import os
from unittest.mock import patch, Mock
import pytest
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


def test_generate_categorization_http_error(llm_client):
    with patch('eco_tracker.api_cache.execute_or_get_from_cache') as mock_execute_or_get_from_cache, \
         patch('requests.post') as mock_post:

        # Mock the decorator to just run the function directly
        def dummy_decorator(*args, **kwargs):
            def wrapper(func):
                def inner(body):
                    return func(body)
                return inner
            return wrapper

        mock_execute_or_get_from_cache.side_effect = dummy_decorator

        # Simulate HTTP error
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Server Error"
        mock_post.return_value = mock_response

        with pytest.raises(exceptions.HTTPException) as exc_info:
            llm_client.generate_categorization(product="TestProduct", num_of_categories=15)

        assert exc_info.value.status_code == 500
