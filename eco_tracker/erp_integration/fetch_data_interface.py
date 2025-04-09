from abc import abstractmethod, ABC
from dataclasses import dataclass

@dataclass
class Data:
	source: str
	data: list

class DataFetcher(ABC):

	@abstractmethod
	def fetch_data_from_source(self) -> Data:
		raise NotImplementedError()