"""
Test fuzzy search functionality
"""

from lhatolcsc.api.client import LCSCClient

# Create client with mock server credentials
client = LCSCClient(
    api_key="test_api_key_12345",
    api_secret="test_api_secret_67890",
    base_url="http://localhost:5000"
)

print("=" * 80)
print("Testing Fuzzy Multi-Token Search")
print("=" * 80)

# Test 1: Search for "100k 0603" (should find 100kΩ resistors in 0603 package)
print("\n1. Searching for '100k 0603' (multi-token search)...")
result = client.search_products(keyword="100k 0603", page_size=10)
print(f"   Found {result.total} products")
if result.products:
    for i, product in enumerate(result.products[:5], 1):
        print(f"   {i}. {product.product_code} - {product.product_name}")
        print(f"      Package: {product.package_type}, Brand: {product.manufacturer}")

# Test 2: Search for "yageo 0201" (brand + package)
print("\n2. Searching for 'yageo 0201' (brand + package)...")
result = client.search_products(keyword="yageo 0201", page_size=10)
print(f"   Found {result.total} products")
if result.products:
    for i, product in enumerate(result.products[:3], 1):
        print(f"   {i}. {product.product_code} - {product.product_name}")
        print(f"      Package: {product.package_type}, Brand: {product.manufacturer}")

# Test 3: Search for "ceramic 10v" (type + voltage)
print("\n3. Searching for 'ceramic 10v' (type + voltage in description)...")
result = client.search_products(keyword="ceramic 10v", page_size=10)
print(f"   Found {result.total} products")
if result.products:
    for i, product in enumerate(result.products[:3], 1):
        print(f"   {i}. {product.product_code} - {product.product_name}")

# Test 4: Search for "0402 samsung" (package + brand)
print("\n4. Searching for '0402 samsung' (package + brand)...")
result = client.search_products(keyword="0402 samsung", page_size=5)
print(f"   Found {result.total} products")

# Test 5: Old-style single keyword still works
print("\n5. Searching for 'C100773' (single product code)...")
result = client.search_products(keyword="C100773", page_size=1)
print(f"   Found {result.total} products")
if result.products:
    product = result.products[0]
    print(f"   {product.product_code} - {product.product_name}")

print("\n" + "=" * 80)
print("Fuzzy search test completed!")
print("=" * 80)
