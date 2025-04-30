class EmissionFactorNotFound(Exception):
		def __init__(self, activity_id: str):
				self.activity_id = activity_id
				super().__init__(f"Emission factor not found for activity_id: {activity_id}")

		def __str__(self):
				return f"No emission factor found for activity_id: {self.activity_id}"

class EmissionFactorNotFoundForProduct(Exception):
		def __init__(self, product_name: str, tried_search_queries: list[str]):
				self.product_name = product_name
				self.tried_search_queries = tried_search_queries
				super().__init__(f"Emission factor not found for product named: {product_name}. Tried search queries: {tried_search_queries}")

class EmissionFactorInfoNotFound(Exception):
		def __init__(self, search_query: str):
				self.search_query = search_query
				super().__init__(f"Emission factor info not found for search_query: {search_query}")

		def __str__(self):
				return f"No emission factor info found for search_query: {self.search_query}"
  
class UnsupportedUnit(Exception):
		def __init__(self, unit: str):
				self.unit = unit
				super().__init__(f"Unsupported unit: {unit}")

		def __str__(self):
			return f"Unsupported unit: {self.unit}"