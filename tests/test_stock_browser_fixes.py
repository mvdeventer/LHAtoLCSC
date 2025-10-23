"""
Test script for enhanced stock browser functionality.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lhatolcsc.gui.currency_converter import currency_converter
import re


def test_price_extraction():
    """Test the price extraction logic used in sorting."""
    
    def get_price(val):
        if not val or val == '':
            return None
        try:
            # Remove currency symbols except decimal point
            numeric_str = re.sub(r'[^\d.-]', '', val)
            if numeric_str:
                return float(numeric_str)
            return None
        except (ValueError, TypeError):
            return None
    
    print("🧪 Testing Price Extraction for Sorting")
    print("=" * 50)
    
    # Test various currency formats
    test_prices = [
        "$1.2345",     # USD
        "€1.0641",     # EUR  
        "£0.9246",     # GBP
        "¥187",        # JPY (no decimals)
        "¥8.7649",     # CNY
        "C$1.7283",    # CAD
        "CHF1.1234",   # CHF
        "kr10.50",     # SEK/NOK/DKK
        "",            # Empty
        "N/A",         # Invalid
    ]
    
    print("Testing price extraction from various currency formats:")
    for price_str in test_prices:
        extracted = get_price(price_str)
        print(f"  '{price_str}' → {extracted}")
    
    print("\n🎯 Testing sorting logic:")
    
    # Test sorting with mixed currencies
    mixed_prices = ["$1.23", "€2.45", "£0.99", "", "¥150", "CHF3.45"]
    price_tuples = []
    
    for price_str in mixed_prices:
        extracted = get_price(price_str)
        if extracted is not None:
            price_tuples.append((extracted, price_str, f"item_{price_str}"))
    
    print(f"\nBefore sorting: {[x[1] for x in price_tuples]}")
    
    # Sort ascending (low to high)
    price_tuples.sort(key=lambda x: x[0], reverse=False)
    print(f"Ascending:      {[x[1] for x in price_tuples]}")
    
    # Sort descending (high to low)
    price_tuples.sort(key=lambda x: x[0], reverse=True)
    print(f"Descending:     {[x[1] for x in price_tuples]}")
    
    print("\n✅ Price extraction and sorting test completed!")


def test_currency_symbols():
    """Test currency symbol display in headers."""
    print("\n💱 Testing Currency Header Symbols")
    print("=" * 50)
    
    test_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CAD', 'CHF']
    
    for currency in test_currencies:
        symbol = currency_converter.get_currency_symbol(currency)
        header_example = f"{symbol} (1+)"
        print(f"  {currency}: '{header_example}'")
    
    print("\n✅ Currency symbol test completed!")


if __name__ == "__main__":
    test_price_extraction()
    test_currency_symbols()