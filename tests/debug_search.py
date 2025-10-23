#!/usr/bin/env python3
"""
Debug script to check search results structure.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from mock_db import MockDatabase

def debug_search_results():
    """Debug what search_products returns."""
    print("Debugging search results structure...")
    
    # Initialize database
    db = MockDatabase()
    
    # Test search
    results = db.search_products("resistor", page=1, page_size=2)
    
    print(f"Type: {type(results)}")
    print(f"Keys: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}")
    if 'productList' in results and results['productList']:
        print(f"First product keys: {list(results['productList'][0].keys())}")
        print(f"First product: {results['productList'][0]}")
    else:
        print("No products in list")
    print(f"Total results: {results.get('total', 'Unknown')}")

if __name__ == "__main__":
    debug_search_results()