"""Quick test to verify categories are being returned from database."""
import sys
sys.path.insert(0, 'tests')

from mock_db import MockDatabase

db = MockDatabase('tests/mock_products.db')
result = db.search_products('resistor', 1, 5)

print(f"Found {result['total']} resistors")
print("\nSample products with categories:")
for p in result['productList']:
    category = p.get('parentCatalogName', '(no category)')
    print(f"  {p['productCode']} - {p.get('productModel', 'N/A')}: {category}")

db.close()
