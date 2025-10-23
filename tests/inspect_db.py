"""
Inspect database structure to understand JSON format.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

try:
    from mock_db import MockDatabase
    
    def inspect_database():
        """Inspect the database structure."""
        print("🔍 Inspecting Database Structure")
        print("=" * 50)
        
        db_path = os.path.join('tests', 'mock_products.db')
        if not os.path.exists(db_path):
            print(f"❌ Database not found at {db_path}")
            return
        
        db = MockDatabase(db_path)
        
        # Get a sample product
        cursor = db.conn.cursor()
        cursor.execute("SELECT product_data FROM products LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            product_data = json.loads(row[0])
            print("📦 Sample Product JSON Structure:")
            print("-" * 50)
            
            # Print keys and sample values
            for key, value in product_data.items():
                if isinstance(value, list) and len(value) > 0:
                    print(f"{key}: [{type(value[0]).__name__}] (length: {len(value)})")
                    if key == 'priceList' and len(value) > 0:
                        print(f"  First price tier: {value[0]}")
                elif isinstance(value, dict):
                    print(f"{key}: {{{', '.join(value.keys())}}}")
                else:
                    print(f"{key}: {type(value).__name__} = {str(value)[:100]}")
            
            print("\n📊 Checking specific fields:")
            print(f"Stock Number: {product_data.get('stockNumber', 'NOT FOUND')}")
            print(f"Product Code: {product_data.get('productCode', 'NOT FOUND')}")
            
            if 'productPriceList' in product_data:
                print(f"Price List Length: {len(product_data['productPriceList'])}")
                if len(product_data['productPriceList']) > 0:
                    first_price = product_data['productPriceList'][0]
                    print(f"First Price Tier Keys: {list(first_price.keys())}")
                    print(f"First Price Tier: {first_price}")
            else:
                print("❌ productPriceList not found")
        
        db.close()
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()


if __name__ == "__main__":
    inspect_database()