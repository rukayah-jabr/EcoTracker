import os

from dotenv import load_dotenv

from eco_tracker.erp_integration.fetch_data_interface import Data, DataFetcher
from eco_tracker.erp_integration.fetch_data_filter import FetchDataFilter
from eco_tracker.erp_integration.odoo import Odoo
from eco_tracker.distance_estimation.open_route_service import get_distance_from_delivery_address
from eco_tracker.categorization.categorizer_interface import Categorizer
from eco_tracker.categorization.climatiq_categorization import ClimatiqCategorizer
from eco_tracker.categorization.climatiq_categorization_filter import ClimatiqCategorizerFilter
from eco_tracker.product import Product
from eco_tracker.emission_factors.climatiq import Climatiq
from eco_tracker.emission_factors.emission_factors_interface import EmissionFactorsFetcher
from eco_tracker.emission_factors.emission_factors_filter import EmissionFactorsFilter
from eco_tracker.pipeline import Pipeline

load_dotenv()
CLIMATIQ_API_KEY=os.getenv("CLIMATIQ_API_KEY")
LLM_API_KEY=os.getenv("LLM_API_KEY")

def main():

    odoo: DataFetcher = Odoo()
    groq_categorizer: Categorizer = ClimatiqCategorizer(LLM_API_KEY)
    climatiq: EmissionFactorsFetcher = Climatiq(CLIMATIQ_API_KEY)

    # Define product pipeline
    pipeline = Pipeline[Product](
        ClimatiqCategorizerFilter(groq_categorizer),
        EmissionFactorsFilter(climatiq, "^20"),
    )

    # Get data
    OdooData = FetchDataFilter(odoo)
    OdooData()

    # Run pipline over each item in data
    # TODO: adapt the FetchDataFilter to work within the pipeline?

    for index, product in enumerate(OdooData.data):
        if index == 5: # limit for testing purposes
            break

        # Run pipeline
        pipeline(product)

        # show returned categories and emissions factors
        print(product.climatiq_categories)
        print(product.emission_factor)

        # show cleaned supplier addresses and get distance calculation
        print(product.supplier_address)
        print(f"Distance: {get_distance_from_delivery_address(odoo.delivery_address, product.supplier_address)}km")
        
        print("==================")

if __name__ == "__main__":
    main()