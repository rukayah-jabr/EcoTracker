from abc import ABC, abstractmethod

from eco_tracker.product import Product


class PurchaseEmissionsEstimator(ABC):

    @abstractmethod
    def estimate_emissions(self, product: Product) -> float:
        raise NotImplementedError()
