"""
Test script to verify description search functionality
"""

from lhatolcsc.api.client import LCSCClient

# Create client with mock server credentials
client = LCSCClient(
    api_key="test_api_key_12345",
    api_secret="test_api_secret_67890",
    base_url="http://localhost:5000"
)

print("=" * 80)
print("Testing Description Search Functionality")
print("=" * 80)

# Test 1: Search for "multilayer" (should find in descriptions)
print("\n1. Searching for 'multilayer' (should find capacitors)...")
result = client.search_products(keyword="multilayer", page_size=5)
print(f"   Found {result.total} products")
if result.products:
    for i, product in enumerate(result.products[:3], 1):
        desc = product.description[:100] if product.description else 'N/A'
        print(f"   {i}. {product.product_code} - {product.product_name}")
        print(f"      Description: {desc}...")

# Test 2: Search for "temperature coefficient" (should find in descriptions)
print("\n2. Searching for 'temperature coefficient' (should find resistors)...")
result = client.search_products(keyword="temperature coefficient", page_size=5)
print(f"   Found {result.total} products")
if result.products:
    for i, product in enumerate(result.products[:3], 1):
        desc = product.description[:100] if product.description else 'N/A'
        print(f"   {i}. {product.product_code} - {product.product_name}")
        print(f"      Description: {desc}...")

# Test 3: Search for "microcontroller" (should find in descriptions)
print("\n3. Searching for 'microcontroller' (should find MCUs)...")
result = client.search_products(keyword="microcontroller", page_size=5)
print(f"   Found {result.total} products")
if result.products:
    for i, product in enumerate(result.products[:3], 1):
        desc = product.description[:100] if product.description else 'N/A'
        print(f"   {i}. {product.product_code} - {product.product_name}")
        print(f"      Description: {desc}...")

# Test 4: Search for "RoHS compliant" (should find many components)
print("\n4. Searching for 'RoHS compliant' (should find many components)...")
result = client.search_products(keyword="RoHS compliant", page_size=5)
print(f"   Found {result.total} products")

# Test 5: Regular search still works (product code)
print("\n5. Searching for 'C100773' (product code search)...")
result = client.search_products(keyword="C100773", page_size=5)
print(f"   Found {result.total} products")
if result.products:
    product = result.products[0]
    print(f"   {product.product_code} - {product.product_name}")
    print(f"   Brand: {product.manufacturer}, Package: {product.package_type}")
    print(f"   Description: {product.description[:150]}...")

print("\n" + "=" * 80)
print("Test completed successfully!")
print("=" * 80)
