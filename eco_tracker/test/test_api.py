import pytest
from fastapi.testclient import TestClient

from eco_tracker.api import app


@pytest.fixture
def test_api_client() -> TestClient:
    return TestClient(app)
    
def test_calculate_emissions(test_api_client: TestClient):
    delivery_date_from = '2024-08-02' # a data with just 2 products
    delivery_date_to = '2024-08-02'
    confidence = 0.7
  
    response = test_api_client.get(f"/calculate-emissions?url=http://localhost:8069&start_date={delivery_date_from}&end_date={delivery_date_to}&confidence={confidence}")
    assert response.status_code == 200
    
    body = response.json()
    assert body is not None
    
    for product in body:
        assert product['delivered_date'] >= delivery_date_from
        assert product['delivered_date'] <= delivery_date_to
        assert confidence == 0.7
