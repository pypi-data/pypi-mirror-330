from abc import ABC, abstractmethod
import httpx


class APIClient(ABC):
    """Base class for API clients using httpx."""

    BASE_URL: str = ""

    def __init__(self):
        self.auth_token = None
        self.headers = {}

    @abstractmethod
    def authenticate(self):
        """Method that must be implemented by subclasses to handle authentication."""
        pass

    def call_api(self, endpoint: str, data: dict = None, method: str = "POST"):
        """Generic API call method."""
        if not self.auth_token:
            self.authenticate()
            if not self.auth_token:
                raise ValueError("Authentication failed. No token available.")
        
        url = f"{self.BASE_URL}/{endpoint}"
        self.headers["Authorization"] = f"Bearer {self.auth_token}"
        
        try:
            with httpx.Client(timeout=10) as client:
                response = client.request(method, url, json=data, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            raise RuntimeError(f"API request error: {e}")
