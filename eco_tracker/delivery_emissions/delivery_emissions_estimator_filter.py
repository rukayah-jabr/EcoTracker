from eco_tracker.delivery_emissions.delivery_emissions_estimator_interface import DeliveryEmissionsEstimator
from eco_tracker.pipeline import NextStep, PipelineStep
from eco_tracker.product import Product
from eco_tracker.utils.log import get_logger

logger = get_logger(__name__)

class DeliveryEmissionsEstimatorFilter(PipelineStep):

  def __init__(self, delivery_emissions_estimator: DeliveryEmissionsEstimator):
    self.delivery_emissions_estimator = delivery_emissions_estimator

  def __call__(self, product: Product, next_step: NextStep) -> None:
    print("----------------------------------------\nPIPELINE STEP: Estimate Delivery/Transport Emissions")
    if not self._is_all_needed_data_available(product):
      logger.error(f"Delivery emissions estimation not calculated because distance estimation or weight estimation failed for product {product.description}")
      product.failed_steps.delivery_emissions_estimation = True
      next_step(product)
      return None
    
    # Type narrowing - we know these are not None because of _is_all_needed_data_available check
    distance: float = product.delivery_distance # type: ignore
    weight: float = product.weight # type: ignore
    emission_factor: EmissionFactor = product.delivery_emission_factor # type: ignore
    
    product.co2_transport = self.delivery_emissions_estimator.estimate_delivery_emissions(distance, weight, emission_factor)
    next_step(product)
    
  def _is_all_needed_data_available(self, product: Product) -> bool:
    return (product.failed_steps.distance_estimation == False and
            product.failed_steps.weight_estimation == False and
            product.delivery_distance is not None and
            product.weight is not None and
            product.delivery_emission_factor is not None)