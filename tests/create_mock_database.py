"""
Convert Mock Products JSON to SQLite Database

This script converts the mock_products_large.json file to a SQLite database
for much faster searching.

Usage:
    cd tests
    python create_mock_database.py

This will create 'mock_products.db' in the tests directory.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from mock_db import convert_json_to_db

if __name__ == '__main__':
    json_file = 'mock_products_large.json'
    db_file = 'mock_products.db'
    
    print("=" * 60)
    print("Mock Products Database Converter")
    print("=" * 60)
    
    if not os.path.exists(json_file):
        print(f"\n❌ Error: {json_file} not found")
        print("\nPlease ensure you are running this script from the tests/ directory")
        print("and that mock_products_large.json exists.")
        sys.exit(1)
    
    print(f"\nConverting {json_file} to SQLite database...")
    print("This may take a few moments for large files...\n")
    
    try:
        convert_json_to_db(json_file, db_file)
        
        print("\n" + "=" * 60)
        print("✓ Database created successfully!")
        print("=" * 60)
        print(f"\nDatabase file: {db_file}")
        print("\nYou can now use the mock server with fast SQLite searching.")
        print("Simply restart the mock server - it will automatically detect")
        print("and use the database.")
        
    except Exception as e:
        print(f"\n❌ Error creating database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
