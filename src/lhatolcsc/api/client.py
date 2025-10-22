"""
LCSC API Client.

Main client for interacting with LCSC API endpoints.
"""

import logging
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from lhatolcsc.api.auth import LCSCAuth
from lhatolcsc.api.endpoints import LCSCEndpoints
from lhatolcsc.api.models import LCSCProduct, SearchResult


logger = logging.getLogger(__name__)


class LCSCAPIError(Exception):
    """Base exception for LCSC API errors."""
    pass


class LCSCAuthenticationError(LCSCAPIError):
    """Authentication-related errors."""
    pass


class LCSCRateLimitError(LCSCAPIError):
    """Rate limit exceeded errors."""
    pass


class LCSCClient:
    """
    LCSC API Client.
    
    Provides methods for searching products, getting details, and more.
    """
    
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://www.lcsc.com",
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize LCSC API client.
        
        Args:
            api_key: LCSC API key
            api_secret: LCSC API secret
            base_url: Base URL for API endpoints
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url
        self.timeout = timeout
        self.auth = LCSCAuth(api_key, api_secret)
        self.endpoints = LCSCEndpoints()
        
        # Setup session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        logger.info("LCSC API client initialized")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make authenticated request to LCSC API.
        
        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON request body
            
        Returns:
            API response data
            
        Raises:
            LCSCAPIError: For API-related errors
            LCSCAuthenticationError: For authentication failures
            LCSCRateLimitError: For rate limit errors
        """
        url = urljoin(self.base_url, endpoint)
        
        # Add authentication parameters
        auth_params = self.auth.get_auth_params()
        if params:
            params.update(auth_params)
        else:
            params = auth_params
        
        logger.debug(f"Making {method} request to {url}")
        
        try:
            if method.upper() == "GET":
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )
            elif method.upper() == "POST":
                if json_data:
                    json_data.update(auth_params)
                response = self.session.post(
                    url,
                    json=json_data,
                    timeout=self.timeout
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            data = response.json()
            
            # Check API response
            if not data.get("success", False):
                code = data.get("code", 0)
                message = data.get("message", "Unknown error")
                
                # Handle specific error codes
                if code == 430:
                    raise LCSCAuthenticationError(f"Authentication failed: {message}")
                elif code in [437, 438]:
                    raise LCSCRateLimitError(f"Rate limit exceeded: {message}")
                else:
                    raise LCSCAPIError(f"API error {code}: {message}")
            
            logger.debug(f"Request successful: {url}")
            return data.get("result", {})
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout: {url}")
            raise LCSCAPIError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise LCSCAPIError(f"Request failed: {str(e)}")
    
    def search_products(
        self,
        keyword: str,
        match_type: str = "fuzzy",
        current_page: int = 1,
        page_size: int = 30,
        is_available: bool = False,
        is_pre_sale: bool = False
    ) -> SearchResult:
        """
        Search for products by keyword.
        
        Args:
            keyword: Search keyword (SKU/MPN/Category/Manufacturer)
            match_type: "exact" or "fuzzy" matching
            current_page: Page number (1-indexed)
            page_size: Results per page (max 100 for real API, unlimited for mock)
            is_available: Only return in-stock items
            is_pre_sale: Include pre-sale items
            
        Returns:
            SearchResult with products and pagination info
        """
        logger.info(f"Searching products: keyword='{keyword}', match_type={match_type}, page_size={page_size}")
        
        # Cap at 100 for real LCSC API, but allow larger values for mock server
        # Check if using mock server (localhost)
        max_page_size = 1000 if 'localhost' in self.base_url or '127.0.0.1' in self.base_url else 100
        
        params = {
            "keyword": keyword,
            "match_type": match_type,
            "current_page": current_page,
            "page_size": min(page_size, max_page_size),
            "is_available": is_available,
            "is_pre_sale": is_pre_sale
        }
        
        result = self._make_request("GET", self.endpoints.SEARCH_PRODUCT, params=params)
        
        products = [
            LCSCProduct.from_dict(p) for p in result.get("productList", [])
        ]
        
        return SearchResult(
            products=products,
            total=result.get("total", 0),
            current_page=current_page,
            page_size=page_size
        )
    
    def get_product_details(self, product_number: str) -> Optional[LCSCProduct]:
        """
        Get detailed information for a specific product.
        
        Args:
            product_number: LCSC product number (e.g., "C2653")
            
        Returns:
            LCSCProduct with full details, or None if not found
        """
        logger.info(f"Getting product details: {product_number}")
        
        params = {"product_number": product_number}
        
        try:
            result = self._make_request(
                "GET",
                self.endpoints.PRODUCT_INFO.format(product_number=product_number),
                params=params
            )
            return LCSCProduct.from_dict(result)
        except LCSCAPIError as e:
            logger.warning(f"Product not found: {product_number} - {e}")
            return None
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """
        Get all product categories.
        
        Returns:
            List of category dictionaries
        """
        logger.info("Getting categories")
        result = self._make_request("GET", self.endpoints.CATEGORY)
        return result.get("categoryList", [])
    
    def get_brands(self) -> List[Dict[str, Any]]:
        """
        Get all manufacturer brands.
        
        Returns:
            List of brand dictionaries
        """
        logger.info("Getting brands")
        result = self._make_request("GET", self.endpoints.BRAND)
        return result.get("brandList", [])
    
    def test_connection(self) -> bool:
        """
        Test API connection and credentials.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try a simple search
            self.search_products("test", page_size=1)
            logger.info("API connection test successful")
            return True
        except Exception as e:
            logger.error(f"API connection test failed: {e}")
            return False
