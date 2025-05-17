
from eco_tracker.distance_estimation.distance_estimation_interface import DistanceEstimator
from eco_tracker.pipeline import NextStep, PipelineStep
from eco_tracker.product import Product
from eco_tracker.utils.log import get_logger

logger = get_logger(__name__)

class DistanceEstimationFilter(PipelineStep):
  
  def __init__(self, distance_estimator: DistanceEstimator):
    self.distance_estimator = distance_estimator

  def __call__(self, product: Product, next_step: NextStep) -> None:
    try:
      product.delivery_distance = self.distance_estimator.get_distance_from_delivery_address(str(product.supplier_address), str(product.delivery_address))
    except Exception as e:
      logger.error(f"Error while estimating delivery distance: {e}")
      product.failed_steps.distance_estimation = True

    next_step(product)
    