"""Check if 3.3k 0603 resistor exists in database"""
import sqlite3
import json

db_path = 'mock_products.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Checking for 3.3k 0603 resistor...")
print("="*60)

# Try different search patterns
searches = [
    ("3.3k AND 0603", "SELECT COUNT(*) FROM products WHERE lower(product_data) LIKE '%3.3k%' AND lower(product_data) LIKE '%0603%'"),
    ("3k3 AND 0603", "SELECT COUNT(*) FROM products WHERE lower(product_data) LIKE '%3k3%' AND lower(product_data) LIKE '%0603%'"),
    ("3300 AND 0603", "SELECT COUNT(*) FROM products WHERE lower(product_data) LIKE '%3300%' AND lower(product_data) LIKE '%0603%'"),
    ("Any 0603 resistors", "SELECT COUNT(*) FROM products WHERE lower(product_data) LIKE '%0603%' AND lower(product_data) LIKE '%resistor%'"),
]

for desc, query in searches:
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"{desc}: {count} products")

# Show some 0603 resistor examples
print("\n" + "="*60)
print("Sample 0603 resistors in database:")
print("="*60)

cursor.execute("""
    SELECT product_data 
    FROM products 
    WHERE lower(product_data) LIKE '%0603%' 
    AND lower(product_data) LIKE '%resistor%'
    LIMIT 10
""")

for row in cursor.fetchall():
    product = json.loads(row[0])
    model = product.get('productModel', '')
    code = product.get('productCode', '')
    name = product.get('productNameEn', product.get('productName', ''))
    print(f"{code} - {model}: {name[:80]}")

conn.close()
