import sqlite3
import json
from collections import Counter

conn = sqlite3.connect('mock_products.db')
cursor = conn.cursor()

print("="*60)
print("Category Information in Database")
print("="*60)

# Get all categories from products
cursor.execute("SELECT product_data FROM products")
categories = []
for row in cursor.fetchall():
    product = json.loads(row[0])
    cat = product.get('parentCatalogName', '')
    if cat:
        categories.append(cat)

# Count categories
category_counts = Counter(categories)

print(f"\nTotal products: {len(categories):,}")
print(f"Unique categories: {len(category_counts)}")
print("\nTop 20 categories:")
for cat, count in category_counts.most_common(20):
    print(f"  {cat}: {count:,} products")

# Show sample products with categories
print("\n" + "="*60)
print("Sample products:")
print("="*60)
cursor.execute("SELECT product_data FROM products LIMIT 5")
for row in cursor.fetchall():
    p = json.loads(row[0])
    print(f"{p.get('productCode')}: {p.get('parentCatalogName', 'NO CATEGORY')}")

conn.close()
