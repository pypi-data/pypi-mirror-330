# Handles API Communication with Glaium Server
# --------------------------------------------------
# Stores your api_key and any authentication headers
# Stores the base_url (or other connection parameters)
# Handles all the HTTP/network operations to the server
# Provides helper methods for error handling

import requests
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Use socket to decide if code is prod or local
class GlaiumClient:
    def __init__(self, auth_token: str, base_url: str = "https://optimizer.glaium.io/api/v1"):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        })

        self.base_url=base_url

    # Handles HTTP communication with Glaium
    # Makes sure we send data as JSON and get response from server
    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None):
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            logger.error(f"HTTP Error {status_code}: {e.response.text}")
            raise ApiError(f"HTTP Error {status_code}: {e.response.text}") from e

        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error occurred: %s", str(e))
            raise NetworkError("Failed to connect to Glaium server.") from e

        except requests.exceptions.Timeout as e:
            logger.error("Request timed out: %s", str(e))
            raise NetworkError("Request to Glaium server timed out.") from e

        except Exception as e:
            logger.error("Unexpected error: %s", str(e))
            raise ApiError(f"Unexpected error: {str(e)}") from e

class GlaiumError(Exception):
    """Base exception for all Glaium Client Errors"""

class AuthenticationError(GlaiumError):
    """Invalid authentication"""

class BadRequestError(GlaiumError):
    """Invalid request parameters"""

class ApiError(GlaiumError):
    """Server-side error"""

class NetworkError(GlaiumError):
    """Network connectivity issues"""

