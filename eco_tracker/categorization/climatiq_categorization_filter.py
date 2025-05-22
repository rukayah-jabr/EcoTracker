from eco_tracker.categorization.categorizer_interface import Categorizer
from eco_tracker.pipeline import NextStep, PipelineStep
from eco_tracker.product import Product
from eco_tracker.utils.log import get_logger

logger = get_logger(__name__)

class ClimatiqCategorizerFilter(PipelineStep):

	def __init__(self, categorizer: Categorizer, num_of_categories: int = 15):
		self.categorizer = categorizer
		self.num_of_categories = num_of_categories

	def __call__(self, product: Product, next_step: NextStep) -> None:
		try:
			product.estimated_categories = self.categorizer.generate_categorization(product.description, self.num_of_categories)
		except Exception as e:
			logger.error(f"Error while generating estimate categories for product {product.description}: {e}")
			product.failed_steps.estimate_categories = True

		next_step(product)
