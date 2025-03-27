from eco_tracker.categorization.categorizer_interface import Categorizer
from eco_tracker.product import Product
from eco_tracker.pipeline import NextStep


class ClimatiqCategorizerFilter:

	def __init__(self, categorizer: Categorizer, num_of_categories: int = 15):
		self.categorizer = categorizer
		self.num_of_categories = num_of_categories

	def __call__(self, product: Product, next_step: NextStep) -> None:
		product.climatiq_categories = self.categorizer.generate_categorization(product.description, self.num_of_categories)
		next_step(product)
