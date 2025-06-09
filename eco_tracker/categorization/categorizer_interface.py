from abc import abstractmethod, ABC


class Categorizer(ABC):

	@abstractmethod
	def generate_categorization(self, product: str, num_of_categories: int = 10, confidence: float = 0.7) -> list:
		raise NotImplementedError()
