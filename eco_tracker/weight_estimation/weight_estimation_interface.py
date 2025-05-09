

from abc import ABC, abstractmethod


class WeightEstimator(ABC):

    @abstractmethod
    def estimate_weight(self, product_description: str) -> float:
      raise NotImplementedError("Subclasses must implement this method")
    
    @abstractmethod
    def estimate_weight_of_quantity(self, product_description: str, quantity: float) -> float:
      raise NotImplementedError("Subclasses must implement this method")
   