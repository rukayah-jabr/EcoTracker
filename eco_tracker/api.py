import os
from datetime import datetime
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Query

import eco_tracker.full_pipeline as full_pipeline

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

pipeline_instance = full_pipeline.FullPipeline(CLIMATIQ_API_KEY, LLM_API_KEY, BREACT_API_KEY, OPEN_ROUTE_SERVICE_API_KEY)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/calculate-emissions")
def calculate_emissions(
    url: Annotated[str, Query(description="The URL of the Odoo instance.")],
    start_date: Annotated[str | None, Query(description="The start date in ISO format.")] = None,
    end_date: Annotated[str | None, Query(description="The end date in ISO format.")] = None,
):
    start_date_parsed: datetime | None = None
    end_date_parsed: datetime | None = None

    if start_date is not None:
        start_date_parsed = datetime.fromisoformat(start_date)
        
    if end_date is not None:
        end_date_parsed = datetime.fromisoformat(end_date)
        
    enriched_products = pipeline_instance.calculate_emissions(url, start_date_parsed, end_date_parsed)
    return enriched_products

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("eco_tracker.api:app", host="0.0.0.0", port=8000, reload=True)