from eco_tracker.product import Product
from eco_tracker.emission_factors.emission_factors_interface import EmissionFactorsFetcher
from eco_tracker.emission_factors.exceptions import EmissionFactorNotFound
from eco_tracker.pipeline import NextStep


class EmissionFactorsFilter:

	def __init__(self, emission_factors_fetcher: EmissionFactorsFetcher, data_version: str):
		self.emission_factors_fetcher = emission_factors_fetcher
		self.data_version = data_version

	def __call__(self, product: Product, next_step: NextStep) -> None:
		for category in product.climatiq_categories:
			try:
				emission_factor = self.emission_factors_fetcher.fetch_emission_factor_from_query(category, self.data_version)
				product.emission_factor = emission_factor
				next_step(product)
				return None
			except EmissionFactorNotFound:
				pass

		raise EmissionFactorNotFound(product.description)
