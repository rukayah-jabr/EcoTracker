from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer
from eco_tracker.emission_factors.emission_factors_interface import EmissionFactorsFetcher
from eco_tracker.emission_factors.exceptions import EmissionFactorNotFound, EmissionFactorNotFoundForProduct
from eco_tracker.pipeline import NextStep, PipelineStep
from eco_tracker.product import Product
from eco_tracker.utils.log import get_logger

logger = get_logger(__name__)

class EmissionFactorsFilter(PipelineStep):

    def __init__(self, emission_factors_fetcher: EmissionFactorsFetcher, data_version: str, categorizer: BreactCategorizer):
        self.emission_factors_fetcher = emission_factors_fetcher
        self.data_version = data_version
        self.categorizer = categorizer

    def __call__(self, product: Product, next_step: NextStep) -> None:
        if product.failed_steps.estimate_categories:
            product.failed_steps.emission_factor_fetching = True
            next_step(product)
            return None

        for category in product.estimated_categories:
            try:
                emission_factor = self.emission_factors_fetcher.fetch_emission_factor_from_query(
                    category, product.unit, self.data_version
                )

                confidence = self.categorizer.get_confidence_for_class(emission_factor.description, product.description)
                if confidence < 0.7:
                    continue  # Skip low-confidence match

                product.emission_factor = emission_factor
                product.estimated_matched_category = category
                next_step(product)
                return None

            except EmissionFactorNotFound:
                continue
            except Exception as e:
                logger.error(f"Error fetching emission factor for product {product.description}: {e}")
                raise e

        logger.error(f"No suitable emission factor found for product {product.description} with categories {product.estimated_categories}")
        product.failed_steps.emission_factor_fetching = True
        next_step(product)