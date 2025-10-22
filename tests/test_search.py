import json

# Load database
with open('mock_products_large.json', encoding='utf-8') as f:
    db = json.load(f)

print(f"Total products: {len(db)}")

# Find resistors
resistors = []
for code, product in list(db.items())[:5000]:
    name = product.get('productName', '').lower()
    if 'resistor' in name or 'res ' in name or name.startswith('res '):
        resistors.append((code, product))
        if len(resistors) >= 5:
            break

print(f"\nFound {len(resistors)} resistors:")
for code, p in resistors:
    print(f"  {code}: {p.get('productName')[:70]}")

# Check what C201859 actually is
if 'C201859' in db:
    p = db['C201859']
    print(f"\nC201859 (matched 'resistor' with 48% score):")
    print(f"  Name: {p.get('productName')}")
    print(f"  Model: {p.get('productModel')}")
    print(f"  Category: {p.get('parentCatalogName', 'N/A')}")
