from abc import ABC, abstractmethod

from eco_tracker.product import EmissionFactor


class EmissionFactorsTransportationFetcher(ABC):

    @abstractmethod
    def fetch_emission_factors_transportation(self, transportation_type: str | None) -> EmissionFactor:
      raise NotImplementedError("Subclasses must implement this method")