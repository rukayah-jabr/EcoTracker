from eco_tracker.pipeline import PipelineStep, NextStep
from eco_tracker.product import Product
from eco_tracker.categorization.breact.breact_categorization import BreactCategorizer

class BreactFECategorizationFilter(PipelineStep):
    def __init__(self, categorizer: BreactCategorizer):
        self.categorizer = categorizer

    def __call__(self, product: Product, next_step: NextStep) -> None:
        try:
            categories = self.categorizer.generate_categorization(product.description)
            if categories:
                product.category = categories[0]
        except Exception:
            product.category = "others"
        next_step(product)