from abc import ABC, abstractmethod
from dataclasses import dataclass

from eco_tracker.product import EmissionFactor


class EmissionFactorsFetcher(ABC):

	@abstractmethod
	def fetch_emission_factor_from_query(self, query: str, unit: str, data_version: str) -> EmissionFactor:
		raise NotImplementedError()