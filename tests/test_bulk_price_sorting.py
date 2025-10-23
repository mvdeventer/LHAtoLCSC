#!/usr/bin/env python3
"""
Test script to verify bulk price sorting in search results.
This script tests that components are sorted by their cheapest bulk price first.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from mock_db import MockDatabase

def get_bulk_price(product_data):
    """Extract the cheapest price at the highest quantity break."""
    try:
        price_list = product_data.get('productPriceList', [])
        if not price_list:
            return float('inf')
        
        # Find the highest quantity break with valid price
        best_price = float('inf')
        highest_qty = 0
        
        for price_tier in price_list:
            try:
                qty = int(price_tier.get('endAmount', 0))
                price = float(price_tier.get('productPrice', 0))
                
                if price > 0 and qty >= highest_qty:
                    if qty > highest_qty or price < best_price:
                        highest_qty = qty
                        best_price = price
            except (ValueError, TypeError):
                continue
        
        return best_price if best_price != float('inf') else 0
    except Exception:
        return 0

def test_bulk_price_sorting():
    """Test that search results are sorted by bulk pricing."""
    print("Testing bulk price sorting...")
    
    # Initialize database
    db = MockDatabase()
    
    # Test search for resistors (common components with bulk pricing)
    search_term = "resistor"
    results = db.search_products(search_term, page=1, page_size=10)
    
    print(f"\nSearch results for '{search_term}' (sorted by bulk price):")
    print("-" * 80)
    
    previous_bulk_price = 0
    
    for i, product in enumerate(results['productList'], 1):
        product_data = product  # Product data is directly in the list item
        product_code = product_data.get('productCode', 'Unknown')
        stock = product_data.get('stockNumber', 0)
        bulk_price = get_bulk_price(product_data)
        
        # Get price list for display
        price_list = product_data.get('productPriceList', [])
        price_tiers = []
        for tier in price_list:
            qty = tier.get('endAmount', 0)
            price = tier.get('productPrice', 0)
            if price > 0:
                price_tiers.append(f"{qty}+: ${price}")
        
        print(f"{i:2}. {product_code}")
        print(f"    Stock: {stock:,}")
        print(f"    Bulk Price: ${bulk_price:.6f}")
        print(f"    Price Tiers: {' | '.join(price_tiers[:3])}")
        
        # Verify sorting (bulk price should be ascending)
        if i > 1 and bulk_price < previous_bulk_price:
            print(f"    ⚠️  WARNING: Bulk price ${bulk_price:.6f} < previous ${previous_bulk_price:.6f}")
        
        previous_bulk_price = bulk_price
        print()
    
    print(f"Total results: {results['total']}")
    print(f"Current page: {results['current_page']}")

def test_category_bulk_sorting():
    """Test bulk sorting in category browsing."""
    print("\nTesting bulk price sorting in all products...")
    
    db = MockDatabase()
    
    # Test browsing all products (since category_id not supported)
    results = db.search_products("", page=1, page_size=5)
    
    print("\nAll products browsing results (sorted by bulk price):")
    print("-" * 60)
    
    if not results['productList']:
        print("No results found - database might be empty")
        return
    
    for i, product in enumerate(results['productList'], 1):
        product_data = product  # Product data is directly in the list item
        product_code = product_data.get('productCode', 'Unknown')
        bulk_price = get_bulk_price(product_data)
        stock = product_data.get('stockNumber', 0)
        
        print(f"{i}. {product_code} - Bulk: ${bulk_price:.6f} - Stock: {stock:,}")

if __name__ == "__main__":
    try:
        test_bulk_price_sorting()
        test_category_bulk_sorting()
        print("\n✅ Bulk price sorting test completed!")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()