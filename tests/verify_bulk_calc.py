#!/usr/bin/env python3
"""
Verify bulk price calculation for a specific product.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from mock_db import MockDatabase

def verify_bulk_price_calculation():
    """Verify that bulk price calculation is correct."""
    print("Verifying bulk price calculation...")
    
    db = MockDatabase()
    
    # Get the first resistor result
    results = db.search_products("resistor", page=1, page_size=1)
    
    if not results['productList']:
        print("No products found")
        return
    
    product = results['productList'][0]
    product_code = product.get('productCode', 'Unknown')
    price_list = product.get('productPriceList', [])
    
    print(f"\nProduct: {product_code}")
    print("Price tiers:")
    
    highest_qty = 0
    best_bulk_price = float('inf')
    
    for i, tier in enumerate(price_list, 1):
        start_qty = tier.get('startAmount', 0)
        end_qty = tier.get('endAmount', 0)
        price = tier.get('productPrice', 0)
        
        print(f"  {i}. Qty {start_qty}-{end_qty}: ${price}")
        
        # Find highest quantity with valid price
        if price > 0 and end_qty >= highest_qty:
            if end_qty > highest_qty or price < best_bulk_price:
                highest_qty = end_qty
                best_bulk_price = price
    
    print(f"\nCalculated bulk price (at qty {highest_qty}): ${best_bulk_price}")
    print("This should be the cheapest price at the highest quantity break.")

if __name__ == "__main__":
    verify_bulk_price_calculation()