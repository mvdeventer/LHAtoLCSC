"""
LCSC API Authentication module.

Handles signature generation and request authentication.
"""

import hashlib
import secrets
import time
from typing import Dict


class LCSCAuth:
    """
    LCSC API Authentication handler.
    
    Generates required authentication parameters for API requests.
    """
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize authentication handler.
        
        Args:
            api_key: LCSC API key
            api_secret: LCSC API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
    
    def generate_nonce(self, length: int = 16) -> str:
        """
        Generate a random nonce string.
        
        Args:
            length: Length of the nonce (default: 16)
            
        Returns:
            Random hexadecimal string
        """
        return secrets.token_hex(length // 2)
    
    def generate_signature(
        self, 
        timestamp: str, 
        nonce: str
    ) -> str:
        """
        Generate SHA1 signature for API request.
        
        The signature is calculated as:
        sha1("key={key}&nonce={nonce}&secret={secret}&timestamp={timestamp}")
        
        Args:
            timestamp: Unix timestamp as string
            nonce: Random nonce string
            
        Returns:
            SHA1 hash as hexadecimal string
        """
        params = (
            f"key={self.api_key}&"
            f"nonce={nonce}&"
            f"secret={self.api_secret}&"
            f"timestamp={timestamp}"
        )
        return hashlib.sha1(params.encode()).hexdigest()
    
    def get_auth_params(self) -> Dict[str, str]:
        """
        Generate complete authentication parameters for API request.
        
        Returns:
            Dictionary with key, timestamp, nonce, and signature
        """
        timestamp = str(int(time.time()))
        nonce = self.generate_nonce()
        signature = self.generate_signature(timestamp, nonce)
        
        return {
            "key": self.api_key,
            "timestamp": timestamp,
            "nonce": nonce,
            "signature": signature
        }
    
    def validate_credentials(self) -> bool:
        """
        Validate that credentials are properly formatted.
        
        Returns:
            True if credentials appear valid, False otherwise
        """
        if not self.api_key or not self.api_secret:
            return False
        
        if len(self.api_key) < 10 or len(self.api_secret) < 10:
            return False
        
        return True
