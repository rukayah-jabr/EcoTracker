class CoordinatesNotFound(Exception):
		def __init__(self, address):
				self.address = address
				super().__init__(f"Coordinates not found for address: {address}")

		def __str__(self):
				return f"Coordinates not found for address: {self.address}"

class ManyMatchingCoordinatesFound(Exception):
		def __init__(self, address):
				self.address = address
				super().__init__(f"Many matching locations found for address: {address}")

		def __str__(self):
				return f"Many matching locations found for address: {self.address}"

class RouteDistanceFailed(Exception):
		def __init__(self, start, end):
				self.start = start
				self.end = end
				super().__init__(f"Error calculating route between {start} and {end}")

		def __str__(self):
				return f"Error calculating route between {self.start} and {self.end}"