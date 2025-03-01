class ProxyError(Exception):
    """Base class for all proxy related exceptions."""
    pass


class ProxyRetriesExceeded(ProxyError):
    """Raised when all attempts to send a request using a proxy have failed."""
    
    def __init__(self, retries):
        super().__init__(f"{retries} attempts were made to send a request using a proxy and none of them passed. Raising an exception on the backend")


class NoProxiesAvailable(ProxyError):
    """Raised when no proxies are available for the specified connector."""
    
    def __init__(self, connector_id):
        super().__init__(f"No proxies found for connector_id {connector_id}")

class CantGetProxiesFromAPI(Exception):
    """Raised when cant get proxies from api"""
    
    def __init__(self, last_error: str):
        super().__init__(f"Cant get proxies from api. Last error: {last_error}")
