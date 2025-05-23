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

        confidences = {}
        for category in product.estimated_categories:
            try:
                confidence = self.categorizer.get_confidence_for_class(product.description, category)
                if confidence >= 0.7:  # confidence threshold = 0.7, anything lower is discarded
                    confidences[category] = confidence
            except Exception:
                confidences[category] = 0.0

        sorted_categories = sorted(confidences.items(), key=lambda x: x[1], reverse=True)
        product.estimated_categories = [cat for cat, _ in sorted_categories]

        next_step(product)
