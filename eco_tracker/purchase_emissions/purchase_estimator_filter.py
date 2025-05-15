from eco_tracker.pipeline import NextStep
from eco_tracker.product import Product
from eco_tracker.purchase_emissions.purchase_estimator_interface import PurchaseEmissionsEstimator
from eco_tracker.utils.log import get_logger

logger = get_logger(__name__)

class PurchaseEmissionsEstimatorFilter:

    def __init__(self, estimator: PurchaseEmissionsEstimator):
        self.estimator = estimator

    def __call__(self, product: Product, next_step: NextStep) -> None:
        if product.failed_steps.emission_factor_fetching or product.emission_factor is None:
            product.failed_steps.purchase_co2_calculation = True
            next_step(product)
            return None

        try:
            product.co2_purchase = self.estimator.estimate_emissions(product)
        except Exception as e:
            logger.error(f"Error estimating emissions for product {product.description}: {e}")
            product.failed_steps.purchase_co2_calculation = True

        next_step(product)
