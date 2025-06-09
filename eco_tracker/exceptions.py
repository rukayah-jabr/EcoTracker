class HTTPException(Exception):
    def __init__(self, status_code, message="HTTP request failed"):
        self.status_code = status_code
        self.message = f"{message}: {status_code}"
        super().__init__(self.message)

class CacheOnlyException(Exception):
		def __init__(self, url: str):
				self.url = url
				super().__init__(f"No cached response. CACHE_ONLY set to true, skipping fresh call: {url}")

		def __str__(self):
				return f"No cached response. CACHE_ONLY set to true, skipping fresh call: {self.url}"