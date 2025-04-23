import os

from dotenv import load_dotenv

from eco_tracker.erp_integration.fetch_data_interface import Data, DataFetcher
from eco_tracker.erp_integration.fetch_data_filter import FetchDataFilter
from eco_tracker.erp_integration.odoo import Odoo

from eco_tracker.categorization.categorizer_interface import Categorizer
from eco_tracker.categorization.climatiq_categorization import ClimatiqCategorizer
from eco_tracker.categorization.climatiq_categorization_filter import ClimatiqCategorizerFilter
from eco_tracker.categorization.breact_categorization import BreactCategorizer
from eco_tracker.product import Product
from eco_tracker.emission_factors.climatiq import Climatiq
from eco_tracker.emission_factors.emission_factors_interface import EmissionFactorsFetcher
from eco_tracker.emission_factors.emission_factors_filter import EmissionFactorsFilter
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
    #TODO: add a step for reordering
    pipeline = Pipeline[Product](
        ClimatiqCategorizerFilter(groq_categorizer),
        EmissionFactorsFilter(climatiq, "^20"),
    )

    # Get data
    OdooData = FetchDataFilter(odoo)
    OdooData()

    # Run pipline over each item in data
    # TODO: adapt the FetchDataFilter to work within the pipeline?
    # TODO: standardize the data schema in odoo.fetch_data_from_source
    for index, item in enumerate(OdooData.data):
        if index == 10: # limit to 10 for testing purposes
            break

        product = Product(
            description=item['name'],
            unit="unit",
            quantity=item['product_uom_qty'],
            price=item['price_unit'],
            status="status",
            climatiq_categories=[],
            category="category",
            emission_factor=None,
            co2e=0,
        )

        # Run pipeline
        pipeline(product)
        print(product.climatiq_categories)
        print(product.emission_factor)

        #a small try out for the breact categorizer
        breact_categories = breact_categorizer.generate_categorization(product.description)
        print(f"[Breact] Categorization for '{product.description}': {breact_categories[0]}")
        breact_confidence = breact_categorizer.get_confidence_for_class(product.description, breact_categories[0])
        print(f"[Breact] Conficende for '{breact_categories[0]}': {breact_confidence}")

if __name__ == "__main__":
    main()