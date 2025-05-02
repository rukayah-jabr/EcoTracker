import os

from dotenv import load_dotenv

from eco_tracker.erp_integration.fetch_data_interface import Data, DataFetcher
from eco_tracker.erp_integration.fetch_data_filter import FetchDataFilter
from eco_tracker.erp_integration.odoo import Odoo
from eco_tracker.distance_estimation.open_route_service import get_distance_from_delivery_address
from eco_tracker.categorization.categorizer_interface import Categorizer
from eco_tracker.categorization.climatiq_categorization import ClimatiqCategorizer
from eco_tracker.categorization.climatiq_categorization_filter import ClimatiqCategorizerFilter
from eco_tracker.categorization.breact_categorization import BreactCategorizer
from eco_tracker.product import Product
from eco_tracker.emission_factors.climatiq import Climatiq
from eco_tracker.emission_factors.emission_factors_interface import EmissionFactorsFetcher
from eco_tracker.emission_factors.emission_factors_filter import EmissionFactorsFilter
from eco_tracker.categorization.reorder_categorization import  CategoryReorderStep
from eco_tracker.pipeline import Pipeline

load_dotenv()
CLIMATIQ_API_KEY=os.getenv("CLIMATIQ_API_KEY")
LLM_API_KEY=os.getenv("LLM_API_KEY")
BREACT_API_KEY=os.getenv("BREACT_API_KEY")

def main():

    odoo: DataFetcher = Odoo()
    groq_categorizer: Categorizer = ClimatiqCategorizer(LLM_API_KEY)
    breact_categorizer: Categorizer = BreactCategorizer(BREACT_API_KEY)
    climatiq: EmissionFactorsFetcher = Climatiq(CLIMATIQ_API_KEY)

    # Define product pipeline
    pipeline = Pipeline[Product](
        ClimatiqCategorizerFilter(groq_categorizer),
        CategoryReorderStep(breact_categorizer),
        EmissionFactorsFilter(climatiq, "^20"),
        # todo: breact  categorizer for determining product.category
    )

    # Get data
    OdooData = FetchDataFilter(odoo)
    OdooData()

    # Run pipline over each item in data
    # TODO: adapt the FetchDataFilter to work within the pipeline?

    for index, product in enumerate(OdooData.data):
        if index == 2: # limit for testing purposes
            break

        # Run pipeline
        pipeline(product)

        # show returned categories and emissions factors
        print(product.climatiq_categories) #this should be sorted now
        print(product.emission_factor)

        #a small try out for the breact categorizer
        breact_categories = breact_categorizer.generate_categorization(product.description)
        print(f"[Breact] Categorization for '{product.description}': {breact_categories[0]}")
        breact_confidence = breact_categorizer.get_confidence_for_class(product.description, breact_categories[0])
        print(f"[Breact] Conficende for '{breact_categories[0]}': {breact_confidence}")

        # show cleaned supplier addresses and get distance calculation
        print(product.supplier_address)
        print(f"Distance: {get_distance_from_delivery_address(odoo.delivery_address, product.supplier_address)}km")

        print("==================")

        
if __name__ == "__main__":
    main()