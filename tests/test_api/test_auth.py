"""Tests for API authentication."""

import hashlib
import pytest

from lhatolcsc.api.auth import LCSCAuth


def test_generate_nonce():
    """Test nonce generation."""
    auth = LCSCAuth("test_key", "test_secret")
    nonce = auth.generate_nonce()
    
    assert len(nonce) == 16
    assert isinstance(nonce, str)


def test_generate_signature():
    """Test signature generation."""
    auth = LCSCAuth("test_key", "test_secret")
    timestamp = "1524662065"
    nonce = "63yeike7dy6c2kjd"
    
    expected_params = f"key=test_key&nonce={nonce}&secret=test_secret&timestamp={timestamp}"
    expected_signature = hashlib.sha1(expected_params.encode()).hexdigest()
    
    signature = auth.generate_signature(timestamp, nonce)
    
    assert signature == expected_signature


def test_get_auth_params():
    """Test authentication parameters generation."""
    auth = LCSCAuth("test_key", "test_secret")
    params = auth.get_auth_params()
    
    assert "key" in params
    assert "timestamp" in params
    assert "nonce" in params
    assert "signature" in params
    
    assert params["key"] == "test_key"
    assert len(params["nonce"]) == 16
    assert len(params["signature"]) == 40  # SHA1 hex length


def test_validate_credentials_valid():
    """Test credential validation with valid credentials."""
    auth = LCSCAuth("valid_api_key_12345", "valid_secret_12345")
    assert auth.validate_credentials() is True


def test_validate_credentials_invalid():
    """Test credential validation with invalid credentials."""
    auth = LCSCAuth("", "")
    assert auth.validate_credentials() is False
    
    auth = LCSCAuth("short", "short")
    assert auth.validate_credentials() is False
