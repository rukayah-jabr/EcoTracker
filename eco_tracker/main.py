import os

from dotenv import load_dotenv

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
    groq_categorizer: Categorizer = ClimatiqCategorizer(LLM_API_KEY)
    climatiq: EmissionFactorsFetcher = Climatiq(CLIMATIQ_API_KEY)

    pipeline = Pipeline[Product](
        ClimatiqCategorizerFilter(groq_categorizer),
        EmissionFactorsFilter(climatiq, "^20"),
    )

    product = Product(
        description="Lenovo Yoga 15",
        unit="unit",
        quantity=1,
        price=1000,
        status="status",
        climatiq_categories=[],
        category="category",
        emission_factor=None,
        co2e=0,
    )

    pipeline(product)

    print(product.climatiq_categories)
    print(product.emission_factor)


if __name__ == "__main__":
    main()