from abc import abstractmethod, ABC


class Categorizer(ABC):

	@abstractmethod
	def generate_categorization(self, product: str, num_of_categories: int = 10) -> list:
		raise NotImplementedError()
