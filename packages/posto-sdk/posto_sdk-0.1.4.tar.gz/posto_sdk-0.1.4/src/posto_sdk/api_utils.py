from typing import Dict, Any
import requests
import logging

logger = logging.getLogger("PostoSDK")

class APIClient:
    """Base API client with common functionality"""
    
    def __init__(self, base_url: str, auth_token: str):
        """Initialize the API client
        
        Args:
            base_url: Base URL of the WordPress instance
            auth_token: Authentication token
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Basic {auth_token}",
            "Content-Type": "application/json"
        }
    
    def _get_endpoint(self, path: str) -> str:
        """Build a full endpoint URL
        
        Args:
            path: API endpoint path (e.g. "/wp-json/fs-poster/v1/channels")
            
        Returns:
            Full endpoint URL
        """
        return f"{self.base_url}{path}"
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an API request with error handling
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests.request
            
        Returns:
            Response JSON data
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        try:
            kwargs.setdefault('headers', self.headers)
            response = requests.request(method, self._get_endpoint(endpoint), **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise

# Common API endpoints
ENDPOINTS = {
    'channels': '/wp-json/fs-poster/v1/channels',
    'composer': '/wp-json/fs-poster/v1/composer',
    'media': '/wp-json/wp/v2/media',
    'network_settings': lambda network: f'/wp-json/fs-poster/v1/social-networks/{network}/settings',
    'schedules': '/wp-json/fs-poster/v1/schedules',
    'schedule_insights': '/wp-json/fs-poster/v1/schedules/insights',
    'schedule_retry': '/wp-json/fs-poster/v1/schedules/retry'
} 