class EmissionFactorNotFound(Exception):
		def __init__(self, activity_id: str):
				self.activity_id = activity_id
				super().__init__(f"Emission factor not found for activity_id: {activity_id}")

		def __str__(self):
				return f"No emission factor found for activity_id: {self.activity_id}"

class EmissionFactorInfoNotFound(Exception):
		def __init__(self, search_query: str):
				self.search_query = search_query
				super().__init__(f"Emission factor info not found for search_query: {search_query}")

		def __str__(self):
				return f"No emission factor info found for search_query: {self.search_query}"