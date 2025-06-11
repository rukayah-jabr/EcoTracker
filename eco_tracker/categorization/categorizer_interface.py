from abc import abstractmethod, ABC


class Categorizer(ABC):

	@abstractmethod
	def generate_categorization(self, product: str, num_of_categories: int = 10, min_emission_factor_confidence: float = 0.7) -> list:
		raise NotImplementedError()
