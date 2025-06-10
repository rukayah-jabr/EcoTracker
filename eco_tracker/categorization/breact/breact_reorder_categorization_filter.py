from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer
from eco_tracker.pipeline import NextStep, PipelineStep
from eco_tracker.product import Product


class CategoryReorderFilter(PipelineStep):
    def __init__(self, categorizer: BreactCategorizer):
        self.categorizer = categorizer

    def __call__(self, product: Product, next_step: NextStep) -> None:
        if product.failed_steps.estimate_categories or not product.estimated_categories: #in case there is no categories
            next_step(product)
            return

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

        next_step(product)