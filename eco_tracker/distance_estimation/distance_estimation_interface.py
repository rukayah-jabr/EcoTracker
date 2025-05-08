from abc import ABC, abstractmethod


class DistanceEstimator(ABC):
  
  @abstractmethod
  def get_distance_from_delivery_address(self, supplier_address: str, delivery_address: str) -> float:
    raise NotImplementedError()