from eco_tracker.product import Product
from eco_tracker.purchase_emissions.exceptions import NotSupportedMeasurementUnit, PurchaseEmissionFactorNotSet
from eco_tracker.purchase_emissions.purchase_estimator_interface import PurchaseEmissionsEstimator


class BasicPurchaseEmissionsEstimator(PurchaseEmissionsEstimator):

  def estimate_emissions(self, product: Product) -> float:
    if product.emission_factor is None:
      raise PurchaseEmissionFactorNotSet(product.description)
    
    match product.emission_factor.activity_unit:
      case '':
        return product.emission_factor.co2e * product.quantity
      case 'l':
        return product.emission_factor.co2e * product.quantity
      case 'eur':
        return product.emission_factor.co2e * product.quantity * product.unit_price
    
    raise NotSupportedMeasurementUnit(product.emission_factor.activity_unit)
