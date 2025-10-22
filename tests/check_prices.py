"""Quick script to check price tier variation and images in the database."""
import json
from pathlib import Path

db_path = Path(__file__).parent / 'mock_products_large.json'
print(f"Loading {db_path}...")
with open(db_path) as f:
    data = json.load(f)

print(f"Total products: {len(data)}\n")

# Check first 5 products
print("Sample products with price tier counts and images:")
print("-" * 80)
for i, (code, product) in enumerate(list(data.items())[:5]):
    tiers = product['productPriceList']
    tier_qties = [t['startAmount'] for t in tiers]
    has_image = 'productImages' in product and product['productImages']
    image_url = product.get('productImages', 'N/A')[:60] if has_image else 'N/A'
    
    print(f"{code}: {product['productName'][:60]}")
    print(f"  Stock: {product['stockNumber']:,}")
    print(f"  Price tiers ({len(tiers)}): {tier_qties}")
    print(f"  Image: {image_url}...")
    print()
