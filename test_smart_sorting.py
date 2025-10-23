"""
Test script for smart search sorting - highest stock and best price first.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

try:
    from mock_db import MockDatabase
    
    def test_smart_sorting():
        """Test the new smart sorting functionality."""
        print("🎯 Testing Smart Search Sorting")
        print("=" * 60)
        print("Criteria: 1. Highest Stock → 2. Best Price → 3. Product Code")
        print("=" * 60)
        
        # Connect to database
        db_path = os.path.join('tests', 'mock_products.db')
        if not os.path.exists(db_path):
            print(f"❌ Database not found at {db_path}")
            return
        
        db = MockDatabase(db_path)
        
        # Test search with keyword
        print("\n🔍 Testing search with keyword 'resistor 0603':")
        results = db.search_products(keyword='resistor 0603', page=1, page_size=10)
        
        print(f"\nFound {results['total']} total results, showing top 10:")
        print("-" * 90)
        print(f"{'Rank':<4} {'Product Code':<12} {'Stock':<8} {'Best Price':<12} {'Description':<40}")
        print("-" * 90)
        
        for i, product in enumerate(results['productList'], 1):
            code = product.get('productCode', 'N/A')
            stock = product.get('stockNumber', 0)
            
            # Find best (minimum) price
            best_price = None
            if 'productPriceList' in product:
                prices = []
                for price_tier in product['productPriceList']:
                    if price_tier.get('productPrice', 0) > 0:
                        prices.append(float(price_tier['productPrice']))
                if prices:
                    best_price = min(prices)
            
            price_str = f"${best_price:.4f}" if best_price else "N/A"
            desc = product.get('productIntroEn', '')[:40]
            
            print(f"{i:<4} {code:<12} {stock:<8} {price_str:<12} {desc:<40}")
        
        print("\n🔍 Testing search with keyword '10k':")
        results = db.search_products(keyword='10k', page=1, page_size=5)
        
        print(f"\nFound {results['total']} total results, showing top 5:")
        print("-" * 90)
        print(f"{'Rank':<4} {'Product Code':<12} {'Stock':<8} {'Best Price':<12} {'Description':<40}")
        print("-" * 90)
        
        for i, product in enumerate(results['productList'], 1):
            code = product.get('productCode', 'N/A')
            stock = product.get('stockNumber', 0)
            
            # Find best (minimum) price
            best_price = None
            if 'productPriceList' in product:
                prices = []
                for price_tier in product['productPriceList']:
                    if price_tier.get('productPrice', 0) > 0:
                        prices.append(float(price_tier['productPrice']))
                if prices:
                    best_price = min(prices)
            
            price_str = f"${best_price:.4f}" if best_price else "N/A"
            desc = product.get('productIntroEn', '')[:40]
            
            print(f"{i:<4} {code:<12} {stock:<8} {price_str:<12} {desc:<40}")
        
        print("\n✅ Smart sorting test completed!")
        print("\n📊 Sorting Logic:")
        print("  1. Products with HIGHEST STOCK appear first")
        print("  2. Among products with same stock, CHEAPEST PRICE appears first")
        print("  3. Finally sorted by product code for consistency")
        
        db.close()
        
except ImportError as e:
    print(f"❌ Could not import mock_db: {e}")
    print("Make sure the mock database is available in the tests directory")
except Exception as e:
    print(f"❌ Error during test: {e}")


if __name__ == "__main__":
    test_smart_sorting()