from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer
from eco_tracker.emission_factors.emission_factors_interface import EmissionFactorsFetcher
from eco_tracker.emission_factors.exceptions import EmissionFactorNotFound, EmissionFactorNotFoundForProduct
from eco_tracker.pipeline import NextStep, PipelineStep
from eco_tracker.product import Product
from eco_tracker.api_cache import cached_api_call, save_to_cache
from eco_tracker.utils.log import get_logger
from eco_tracker.categorization.groq.groq_categorizer import ClimatiqCategorizer
import json
import os

logger = get_logger(__name__)

class EmissionFactorsFilter(PipelineStep):

    def __init__(self, emission_factors_fetcher: EmissionFactorsFetcher, data_version: str, categorizer: BreactCategorizer):
        self.emission_factors_fetcher = emission_factors_fetcher
        self.data_version = data_version
        self.categorizer = categorizer

    def __call__(self, product: Product, next_step: NextStep) -> None:
        print("----------------------------------------\nPIPELINE STEP: Emissions Factors (Purchase)")
        if product.failed_steps.estimate_categories:
            product.failed_steps.emission_factor_fetching = True
            next_step(product)
            return None
        
        if product.estimated_categories is not None:
            for category in product.estimated_categories:
                print(f"Checking category: {category} - {product.unit}")
                try:
                    emission_factor = self.emission_factors_fetcher.fetch_emission_factor_from_query(
                        category, product.unit, self.data_version
                    )

                    confidence = self.categorizer.get_confidence_for_class(emission_factor.description, product.description)
                    print(f"Match confidence: {confidence}")
                    print(f"Confidence threshold: {product.confidence}")
                    if confidence < product.confidence:
                        print(f"Low confidence, skipping: {confidence} for {category}")
                        continue  # Skip low-confidence match
                    
                    print(f"Factor found: {confidence} for {category}")

                    # Save categories to cache for future reuse (if cache doesn't already exist)
                    url = ClimatiqCategorizer(os.getenv("LLM_API_KEY")).get_url()
                    request = json.dumps({"product": product.description, "confidence": product.confidence})
                    if not cached_api_call(url, request):
                        print(f"Saving to cache: {product.description} with conf: {product.confidence}")
                        save_to_cache(url=url, request=request, response=json.dumps(list(product.estimated_categories)))
                    
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