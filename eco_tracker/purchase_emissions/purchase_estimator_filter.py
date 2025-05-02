from eco_tracker.pipeline import NextStep
from eco_tracker.product import Product
from eco_tracker.purchase_emissions.purchase_estimator_interface import PurchaseEmissionsEstimator


class PurchaseEmissionsEstimatorFilter:

    def __init__(self, estimator: PurchaseEmissionsEstimator):
        self.estimator = estimator

    def __call__(self, product: Product, next_step: NextStep) -> None:
        product.co2_purchase = self.estimator.estimate_emissions(product)
        next_step(product)
        