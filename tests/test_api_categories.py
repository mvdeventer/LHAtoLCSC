"""Test mock server API to verify categories are returned."""
import requests
import json
import hmac
import hashlib
import time

# Mock credentials
key = 'test_api_key_12345'
secret = 'test_api_secret_67890'

# Create signature
timestamp = str(int(time.time() * 1000))
nonce = 'test123'
sign_str = f'{key}{timestamp}{nonce}'
signature = hmac.new(secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()

# Headers
headers = {
    'X-API-KEY': key,
    'X-TIMESTAMP': timestamp,
    'X-NONCE': nonce,
    'X-SIGNATURE': signature,
    'Content-Type': 'application/json'
}

# Search for resistors
data = {
    'keyword': 'resistor',
    'currentPage': 1,
    'pageSize': 5
}

try:
    r = requests.post('http://localhost:5000/rest/wmsc2agent/search/product', 
                      headers=headers, json=data, timeout=5)
    
    print(f"Status Code: {r.status_code}")
    
    if r.status_code == 200:
        result = r.json()
        print(f"Total Results: {result['result']['total']}")
        print("\nSample Products:")
        for p in result['result']['productList'][:5]:
            category = p.get('parentCatalogName', '(NO CATEGORY)')
            print(f"  {p['productCode']} - {p.get('productModel', 'N/A')}")
            print(f"    Category: {category}")
    else:
        print(f"Error: {r.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to mock server. Is it running on http://localhost:5000?")
except Exception as e:
    print(f"❌ Error: {e}")
