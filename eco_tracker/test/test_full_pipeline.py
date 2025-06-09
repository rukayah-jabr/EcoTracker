
import os
from datetime import datetime

import pytest
from dotenv import load_dotenv

import eco_tracker.full_pipeline as full_pipeline


@pytest.fixture
def full_pipeline_instance():
  load_dotenv()
  CLIMATIQ_API_KEY=os.getenv("CLIMATIQ_API_KEY")
  LLM_API_KEY=os.getenv("LLM_API_KEY")
  BREACT_API_KEY=os.getenv("BREACT_API_KEY")
  OPEN_ROUTE_SERVICE_API_KEY=os.getenv("OPEN_ROUTE_SERVICE_API_KEY")

  if not CLIMATIQ_API_KEY:
    raise ValueError("CLIMATIQ_API_KEY is not set")

  if not LLM_API_KEY:
    raise ValueError("LLM_API_KEY is not set")

  if not BREACT_API_KEY:
    raise ValueError("BREACT_API_KEY is not set")

  if not OPEN_ROUTE_SERVICE_API_KEY:
    raise ValueError("OPEN_ROUTE_SERVICE_API_KEY is not set")
  
  return full_pipeline.FullPipeline(CLIMATIQ_API_KEY, LLM_API_KEY, BREACT_API_KEY, OPEN_ROUTE_SERVICE_API_KEY)


def test_full_pipeline(full_pipeline_instance):
  
  odoo_url = "http://localhost:8069"
  start_date = datetime.strptime("2024-08-02", "%Y-%m-%d")
  end_date = datetime.strptime("2024-08-02", "%Y-%m-%d")
  confidence = 0.7
  
  enriched_products = full_pipeline_instance.calculate_emissions(odoo_url, start_date, end_date, confidence)
  assert len(enriched_products) > 0