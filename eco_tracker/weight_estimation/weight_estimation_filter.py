from eco_tracker.pipeline import NextStep, PipelineStep
from eco_tracker.product import Product
from eco_tracker.utils.log import get_logger
from eco_tracker.weight_estimation.weight_estimation_interface import WeightEstimator

logger = get_logger(__name__)

class WeightEstimationFilter(PipelineStep):

  def __init__(self, weight_estimator: WeightEstimator):
    self.weight_estimator = weight_estimator
    
  def __call__(self, product: Product, next_step: NextStep) -> None:
    if product.failed_steps.distance_estimation:
      logger.error(f"Weight estimation not calculated because distance estimation failed for product {product.description}")
      product.failed_steps.weight_estimation = True
      next_step(product)
      return None

    try:
      product.weight = self.weight_estimator.estimate_weight_of_quantity(product.description, product.quantity)
    except Exception as e:
      logger.error(f"Error estimating weight for product {product.description}: {e}")
      product.failed_steps.weight_estimation = True
    
    next_step(product)
    return None

