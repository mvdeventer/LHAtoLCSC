"""
Test script for currency conversion functionality.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lhatolcsc.gui.currency_converter import currency_converter


def test_currency_conversion():
    """Test currency conversion functionality."""
    print("🔄 Testing Currency Conversion Functionality")
    print("=" * 50)
    
    # Test getting supported currencies
    currencies = currency_converter.get_supported_currencies()
    print(f"📋 Supported currencies: {len(currencies)}")
    for code, symbol in list(currencies.items())[:10]:  # Show first 10
        print(f"  {code}: {symbol}")
    print("  ... and more")
    print()
    
    # Test updating exchange rates
    print("🌐 Updating exchange rates...")
    success = currency_converter.update_exchange_rates()
    if success:
        print("✅ Exchange rates updated successfully")
        rate_info = currency_converter.get_rate_info()
        print(f"📊 {rate_info}")
    else:
        print("❌ Failed to update exchange rates")
    print()
    
    # Test price conversion
    print("💰 Testing price conversions:")
    test_price_usd = 1.2345
    
    test_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CAD']
    
    for currency in test_currencies:
        formatted_price = currency_converter.format_price(
            test_price_usd, currency)
        converted_price = currency_converter.convert_price(
            test_price_usd, currency)
        symbol = currency_converter.get_currency_symbol(currency)
        
        print(f"  ${test_price_usd:.4f} USD → {formatted_price} ({currency})")
        if converted_price and currency != 'USD':
            rate = converted_price / test_price_usd
            print(f"    Exchange rate: 1 USD = {rate:.4f} {currency}")
    
    print()
    print("✅ Currency conversion test completed!")


if __name__ == "__main__":
    test_currency_conversion()