# LCSC API Documentation

## Overview

This document provides comprehensive information about the LCSC API integration in LHAtoLCSC.

## Base URL

```
https://www.lcsc.com
```

## Authentication

All API requests require authentication using SHA1 signature.

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | string | API key from LCSC |
| `secret` | string | API secret (not sent in request) |
| `timestamp` | string | Unix timestamp |
| `nonce` | string | 16-character random string |
| `signature` | string | SHA1 hash of parameters |

### Signature Generation

```python
signature = sha1(f"key={key}&nonce={nonce}&secret={secret}&timestamp={timestamp}")
```

### Example

```python
from lhatolcsc.api.auth import LCSCAuth

auth = LCSCAuth("your_api_key", "your_api_secret")
params = auth.get_auth_params()
# Returns: {'key': '...', 'timestamp': '...', 'nonce': '...', 'signature': '...'}
```

## Rate Limits

- **Default**: 1,000 requests/day, 200 requests/minute
- **Higher limits**: Contact support@lcsc.com

## Available Endpoints

### 1. Keyword Search API ⭐

**Most Important for This Application**

Search for products by keyword with fuzzy or exact matching.

**Endpoint**: `GET /rest/wmsc2agent/search/product`

**Parameters**:

| Parameter | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| `keyword` | Yes | string | - | SKU/MPN/Category/Manufacturer |
| `match_type` | No | string | `exact` | `exact` or `fuzzy` |
| `current_page` | No | integer | 1 | Page number |
| `page_size` | No | integer | 100 | Results per page (max 100) |
| `is_available` | No | boolean | false | Only in-stock items |
| `is_pre_sale` | No | boolean | false | Include pre-sale items |

**Response**:

```json
{
    "success": true,
    "code": 200,
    "message": "",
    "result": {
        "total": 150,
        "productList": [
            {
                "productCode": "C2653",
                "productModel": "STM32F103C8T6",
                "brandNameEn": "STMicroelectronics",
                "productIntroEn": "ARM Cortex-M3 MCU",
                "stockNumber": 5000,
                "productPriceList": [
                    {
                        "startAmount": 1,
                        "productPrice": 2.5,
                        "currency": "USD"
                    }
                ],
                "pdfUrl": "https://...",
                "productImages": "https://..."
            }
        ]
    }
}
```

**Usage**:

```python
from lhatolcsc.api.client import LCSCClient

client = LCSCClient("api_key", "api_secret")
result = client.search_products(
    keyword="STM32F103",
    match_type="fuzzy",
    page_size=30
)

print(f"Found {result.total} products")
for product in result.products:
    print(f"{product.product_number}: {product.product_name}")
```

### 2. Product Details API

Get detailed information for a specific product.

**Endpoint**: `GET /rest/wmsc2agent/product/info/{product_number}`

**Parameters**:

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `product_number` | Yes | string | LCSC product number (e.g., "C2653") |

**Response**:

```json
{
    "success": true,
    "code": 200,
    "result": {
        "productCode": "C2653",
        "productModel": "STM32F103C8T6",
        "brandNameEn": "STMicroelectronics",
        "productIntroEn": "ARM Cortex-M3 MCU, 64KB Flash, 20KB RAM",
        "stockNumber": 5000,
        "encapStandard": "LQFP-48",
        "productPriceList": [...],
        "pdfUrl": "https://...",
        "productImages": "https://..."
    }
}
```

**Usage**:

```python
product = client.get_product_details("C2653")
if product:
    print(f"Stock: {product.stock}")
    print(f"Price: ${product.unit_price}")
```

### 3. Category API

Get all product categories.

**Endpoint**: `GET /rest/wmsc2agent/category`

**Response**:

```json
{
    "success": true,
    "code": 200,
    "result": {
        "categoryList": [
            {
                "catalogId": 17,
                "catalogName": "Integrated Circuits (ICs)",
                "subCatalogs": [...]
            }
        ]
    }
}
```

### 4. Manufacturer/Brand API

Get all manufacturer information.

**Endpoint**: `GET /rest/wmsc2agent/brand`

**Response**:

```json
{
    "success": true,
    "code": 200,
    "result": {
        "brandList": [
            {
                "brandId": 100,
                "brandName": "STMicroelectronics"
            }
        ]
    }
}
```

## Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 200 | Success | - |
| 412 | Date Is Required | Check timestamp parameter |
| 424 | Key Is Required | Provide API key |
| 425 | nonce Is Required | Provide nonce |
| 426 | timestamp Is Required | Provide timestamp |
| 427 | signature Is Required | Provide signature |
| 428 | Timestamp expired | Timestamp > 60s old |
| 429 | Not Found This Product | Product doesn't exist |
| 430 | Appsecret failed verification | Invalid signature |
| 431 | No access to information | Insufficient permissions |
| 437 | API request rate limit exceeded | Retry after 1 minute |
| 438 | API request rate limit exceeded | Retry after 1 day |

## Best Practices

### 1. Caching

Cache search results to reduce API calls:

```python
from diskcache import Cache

cache = Cache('cache_dir')

def cached_search(keyword):
    key = f"search:{keyword}"
    if key in cache:
        return cache[key]
    
    result = client.search_products(keyword)
    cache.set(key, result, expire=604800)  # 7 days
    return result
```

### 2. Rate Limiting

Implement request throttling:

```python
import time

last_request = 0
MIN_INTERVAL = 0.3  # 300ms between requests

def throttled_request():
    global last_request
    elapsed = time.time() - last_request
    if elapsed < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - elapsed)
    
    result = client.search_products(...)
    last_request = time.time()
    return result
```

### 3. Error Handling

Always handle API errors gracefully:

```python
from lhatolcsc.api.client import LCSCAPIError, LCSCRateLimitError

try:
    result = client.search_products(keyword)
except LCSCRateLimitError:
    print("Rate limit exceeded, waiting...")
    time.sleep(60)
    result = client.search_products(keyword)
except LCSCAPIError as e:
    print(f"API error: {e}")
    result = None
```

## API Client Reference

### LCSCClient

Main client class for API interactions.

**Constructor**:

```python
LCSCClient(
    api_key: str,
    api_secret: str,
    base_url: str = "https://www.lcsc.com",
    timeout: int = 30,
    max_retries: int = 3
)
```

**Methods**:

#### `search_products()`

Search for products by keyword.

```python
search_products(
    keyword: str,
    match_type: str = "fuzzy",
    current_page: int = 1,
    page_size: int = 30,
    is_available: bool = False,
    is_pre_sale: bool = False
) -> SearchResult
```

#### `get_product_details()`

Get details for a specific product.

```python
get_product_details(
    product_number: str
) -> Optional[LCSCProduct]
```

#### `test_connection()`

Test API connection.

```python
test_connection() -> bool
```

## Data Models

### LCSCProduct

Represents an LCSC product.

**Attributes**:

- `product_number`: LCSC part number (e.g., "C2653")
- `product_name`: Product name/model
- `manufacturer`: Manufacturer name
- `manufacturer_part`: Manufacturer part number (MPN)
- `description`: Product description
- `stock`: Available stock quantity
- `price_tiers`: List of price tiers
- `datasheet_url`: Link to datasheet
- `in_stock`: Boolean property for stock availability
- `unit_price`: Lowest unit price

### SearchResult

Container for search results.

**Attributes**:

- `products`: List of LCSCProduct objects
- `total`: Total number of matching products
- `current_page`: Current page number
- `page_size`: Results per page
- `total_pages`: Total number of pages (property)
- `has_more`: Whether more pages available (property)

## Examples

### Example 1: Simple Search

```python
from lhatolcsc.api.client import LCSCClient

client = LCSCClient("your_key", "your_secret")
result = client.search_products("STM32F103C8T6", match_type="exact")

if result.products:
    best_match = result.products[0]
    print(f"Found: {best_match.product_number}")
    print(f"Price: ${best_match.unit_price}")
    print(f"Stock: {best_match.stock}")
```

### Example 2: Fuzzy Search with Alternatives

```python
result = client.search_products("STM32 microcontroller", match_type="fuzzy")

print(f"Found {result.total} matches")
for i, product in enumerate(result.products[:5], 1):
    print(f"{i}. {product.product_number}: {product.product_name}")
    print(f"   ${product.unit_price} - Stock: {product.stock}")
```

### Example 3: Pagination

```python
page = 1
all_products = []

while True:
    result = client.search_products("resistor", page=page, page_size=100)
    all_products.extend(result.products)
    
    if not result.has_more:
        break
    page += 1

print(f"Total products collected: {len(all_products)}")
```

## Support

For API issues or questions:

- **Email**: support@lcsc.com
- **API Documentation**: https://www.lcsc.com/docs/
- **Apply for API Access**: https://www.lcsc.com/agent

---

**Last Updated**: October 21, 2025
