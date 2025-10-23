#!/usr/bin/env python3
"""
Initialize database for testing.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from mock_db import MockDatabase

def init_database():
    """Initialize the database with data."""
    print("Initializing database...")
    
    db = MockDatabase()
    
    # Check if database is empty
    results = db.search_products("", page=1, page_size=1)
    if results['total'] == 0:
        print("Database is empty, loading mock data...")
        # Load from JSON if available
        json_path = os.path.join(os.path.dirname(__file__), 'tests', 'mock_products_large.json')
        if os.path.exists(json_path):
            count = db.import_from_json(json_path)
            print(f"Loaded {count} products")
        else:
            print("No JSON file found, database remains empty")
    else:
        print(f"Database has {results['total']} products")

if __name__ == "__main__":
    init_database()