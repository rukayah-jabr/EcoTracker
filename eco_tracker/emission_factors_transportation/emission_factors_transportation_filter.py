
from eco_tracker.emission_factors_transportation.emission_factors_transportation_interface import EmissionFactorsTransportationFetcher
from eco_tracker.pipeline import NextStep, PipelineStep
from eco_tracker.product import Product


class EmissionFactorsTransportationFilter(PipelineStep):

    def __init__(self, emission_factors_transportation: EmissionFactorsTransportationFetcher):
        self.emission_factors_transportation = emission_factors_transportation

    def __call__(self, product: Product, next_step: NextStep) -> None:
        emission_factor = self.emission_factors_transportation.fetch_emission_factors_transportation(product.delivery_transportation_type)
        product.delivery_emission_factor = emission_factor
        next_step(product)