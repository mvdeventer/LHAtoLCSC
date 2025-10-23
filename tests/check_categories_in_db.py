"""Quick check for category data in database."""
import sqlite3

conn = sqlite3.connect('mock_products.db')
cursor = conn.cursor()

# Check if category column exists and has data
cursor.execute('SELECT product_code, parent_catalog_name FROM products LIMIT 10')
rows = cursor.fetchall()

print('Sample products:')
for row in rows:
    print(f'{row[0]}: {row[1] if row[1] else "(empty)"}')

# Count products with categories
cursor.execute('SELECT COUNT(*) FROM products WHERE parent_catalog_name IS NOT NULL AND parent_catalog_name != ""')
with_cats = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM products')
total = cursor.fetchone()[0]

print(f'\nProducts with categories: {with_cats}/{total}')

conn.close()
