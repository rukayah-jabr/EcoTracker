from abc import abstractmethod, ABC
from dataclasses import dataclass

@dataclass
class EmissionFactor:
	co2e: float
	co2e_unit: str
	activity_unit: str

class EmissionFactorsFetcher(ABC):

	@abstractmethod
	def fetch_emission_factor_from_query(self, query: str, data_version: str) -> EmissionFactor:
		raise NotImplementedError()