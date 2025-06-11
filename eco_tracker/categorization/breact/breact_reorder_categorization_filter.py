from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer
from eco_tracker.pipeline import NextStep, PipelineStep
from eco_tracker.product import Product
from eco_tracker.categorization.groq.groq_categorizer import ClimatiqCategorizer
from eco_tracker.api_cache import cached_api_call
import os
import json
from eco_tracker.utils.log import get_logger

logger = get_logger(__name__)

class CategoryReorderFilter(PipelineStep):
    def __init__(self, categorizer: BreactCategorizer):
        self.categorizer = categorizer

    def __call__(self, product: Product, next_step: NextStep) -> None:
        print("----------------------------------------\nPIPELINE STEP: Reordering of Categorization")
        if product.failed_steps.estimate_categories or not product.estimated_categories: #in case there is no categories
            next_step(product)
            return
        
        # check if reordered categories already saved in cache; this means this step can be skipped since they are already reordered
        url = ClimatiqCategorizer.url
        if cached_api_call(url=url, request=json.dumps({"product": product.description, "confidence": product.min_emission_factor_confidence})):
            next_step(product)
            return

        try:
            # all print statements are only for demo
            confidences = self.categorizer.generate_confidences(product.description, product.estimated_categories)
            # confidence threshold 0.7
            filtered_confidences = {
                cat: conf for cat, conf in confidences.items()
                if cat in product.estimated_categories and conf >= 0.7
            }
            print("Original estimated categories:", product.estimated_categories)
            print("Confidences from API:", confidences)

            sorted_categories = sorted(filtered_confidences.items(), key=lambda x: x[1], reverse=True)
            product.estimated_categories = [cat for cat, _ in sorted_categories]
            print ("this is after reorder:", product.estimated_categories)
        except Exception as e:
            logger.error(f"Error while reordering categories for product {product.description}: {e}")
            product.failed_steps.reorder_categories = True

        next_step(product)