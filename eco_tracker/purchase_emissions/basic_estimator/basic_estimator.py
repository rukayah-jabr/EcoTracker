from eco_tracker.product import Product
from eco_tracker.purchase_emissions.exceptions import NotSupportedMeasurementUnit, PurchaseEmissionFactorNotSet
from eco_tracker.purchase_emissions.purchase_estimator_interface import PurchaseEmissionsEstimator


class BasicPurchaseEmissionsEstimator(PurchaseEmissionsEstimator):

  def estimate_emissions(self, product: Product) -> float:
    if product.emission_factor is None:
      raise PurchaseEmissionFactorNotSet(product.description)
    
    co2_purchase = 0.0
    match product.emission_factor.activity_unit:
      case '':
        co2_purchase = product.emission_factor.co2e * abs(product.quantity)
      case 'l':
        co2_purchase = product.emission_factor.co2e * abs(product.quantity)
      case 'eur':
        co2_purchase = product.emission_factor.co2e * abs(product.quantity) * abs(product.unit_price)
      case _:
        raise NotSupportedMeasurementUnit(product.emission_factor.activity_unit)
    
    if self.check_if_delivery_is_return(product):
      co2_purchase = -co2_purchase
    
    return co2_purchase
  
  
  def check_if_delivery_is_return(self, product: Product) -> bool:
    if not hasattr(product, 'delivery') or product.delivery is None:
      return False
    return product.delivery.type == 'R'
