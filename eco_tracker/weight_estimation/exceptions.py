

class WeightEstimationFailed(Exception):
  def __init__(self, product_description: str):
    self.message = f"Weight estimation failed for product {product_description}"
    super().__init__(self.message)
