class AuthenticationFailed(Exception):
		def __init__(self, url):
				self.url = url
				super().__init__(f"Authentication failed when trying to connect to {url}")

		def __str__(self):
				return f"Authentication failed when trying to connect to {self.url}"
		
class FetchingDataFailed(Exception):
		def __init__(self, url):
				self.url = url
				super().__init__(f"Error fetching data from {url}")

		def __str__(self):
				return f"Error fetching data from {self.url}"
		
class SupplierNotFound(Exception):
		def __init__(self, supplier_id):
				self.supplier_id = supplier_id
				super().__init__(f"Supplier address not found for supplier ID {supplier_id}")

		def __str__(self):
				return f"Supplier address not found for supplier ID {self.supplier_id}"
		
class CoordinatesNotFound(Exception):
		def __init__(self, address):
				self.address = address
				super().__init__(f"Coordinates not found for address: {address}")

		def __str__(self):
				return f"Coordinates not found for address: {self.address}"
		
class RouteDistanceFailed(Exception):
		def __init__(self, start, end):
				self.start = start
				self.end = end
				super().__init__(f"Error calculating route between {start} and {end}")

		def __str__(self):
				return f"Error calculating route between {self.start} and {self.end}"