from eco_tracker.product import Product
from eco_tracker.pipeline import NextStep
from eco_tracker.categorization.breact_categorization import BreactCategorizer


class CategoryReorderStep:
    def __init__(self, categorizer: BreactCategorizer):
        self.categorizer = categorizer

    def __call__(self, product: Product, next_step: NextStep) -> None:
        if not product.climatiq_categories: #in case there is no categories
            next_step(product)
            return

        confidences = {}
        for category in product.climatiq_categories:
            try:
                confidence = self.categorizer.get_confidence_for_class(product.description, category)
                confidences[category] = confidence #assign dict
            except Exception:
                confidences[category] = 0.0

        sorted_categories = sorted(confidences.items(), key=lambda x: x[1], reverse=True)
        product.climatiq_categories = [cat for cat, _ in sorted_categories]

        next_step(product)
