class HTTPException(Exception):
    def __init__(self, status_code, message="HTTP request failed"):
        self.status_code = status_code
        self.message = f"{message}: {status_code}"
        super().__init__(self.message)