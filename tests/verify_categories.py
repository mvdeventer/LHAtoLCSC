"""Quick check to verify category assignments."""
import sqlite3

conn = sqlite3.connect('mock_products.db')
cursor = conn.cursor()

# Check any resistors with categories
cursor.execute('''
    SELECT product_code, product_model, package_type, parent_catalog_name 
    FROM products 
    WHERE parent_catalog_name LIKE '%Resistor%'
    LIMIT 10
''')

print("Sample Resistors with categories:")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]} ({row[2]}): {row[3]}")

print()

# Check any capacitors
cursor.execute('''
    SELECT product_code, product_model, package_type, parent_catalog_name 
    FROM products 
    WHERE parent_catalog_name LIKE '%Capacitor%'
    LIMIT 10
''')

print("Sample Capacitors with categories:")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]} ({row[2]}): {row[3]}")

conn.close()
