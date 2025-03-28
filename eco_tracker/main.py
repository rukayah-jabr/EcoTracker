import os

from dotenv import load_dotenv

from eco_tracker.erp_integration.fetch_data_interface import Data, DataFetcher
from eco_tracker.erp_integration.fetch_data_filter import FetchDataFilter
from eco_tracker.erp_integration.odoo import Odoo
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
    # TO DO: adapt the FetchDataFilter to work within the pipeline?
    # TO DO: standardize the data schema in odoo.fetch_data_from_source
    for index, item in enumerate(OdooData.data):
        if index == 10:
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

    # product = Product(
    #     description="Lenovo Yoga 15",
    #     unit="unit",
    #     quantity=1,
    #     price=1000,
    #     status="status",
    #     climatiq_categories=[],
    #     category="category",
    #     emission_factor=None,
    #     co2e=0,
    # )

    # pipeline(product)

    # print(product.climatiq_categories)
    # print(product.emission_factor)

if __name__ == "__main__":
    main()