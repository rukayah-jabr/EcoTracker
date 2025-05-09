
from abc import ABC, abstractmethod

from eco_tracker.product import EmissionFactor


class DeliveryEmissionsEstimator(ABC):
    
  @abstractmethod
  def estimate_delivery_emissions(self, distance: float, weight: float, emission_factor: EmissionFactor) -> float:
    raise NotImplementedError("Subclasses must implement this method")
