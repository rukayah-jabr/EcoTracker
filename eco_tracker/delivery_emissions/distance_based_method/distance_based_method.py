


from eco_tracker.delivery_emissions.delivery_emissions_estimator_interface import DeliveryEmissionsEstimator
from eco_tracker.delivery_emissions.exceptions import WrongActivityUnitException
from eco_tracker.product import EmissionFactor


class DistanceBasedMethod(DeliveryEmissionsEstimator):

  def estimate_delivery_emissions(self, distance: float, weight: float, emission_factor: EmissionFactor) -> float:
    if emission_factor.activity_unit != "kg-km":
      raise WrongActivityUnitException(emission_factor.activity_unit)
    
    return distance * emission_factor.co2e * weight
