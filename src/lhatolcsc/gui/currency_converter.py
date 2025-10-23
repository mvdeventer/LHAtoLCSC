"""
Currency conversion utilities for stock browser.
"""

import requests
import logging
from typing import Dict, Optional
import threading
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class ExchangeRates:
    """Exchange rates from USD to other currencies."""
    rates: Dict[str, float]
    last_updated: datetime
    
    def is_expired(self, max_age_minutes: int = 60) -> bool:
        """Check if rates are expired."""
        time_diff = datetime.now() - self.last_updated
        return time_diff > timedelta(minutes=max_age_minutes)


class CurrencyConverter:
    """Real-time currency converter using free exchange rate API."""
    
    def __init__(self):
        self.exchange_rates: Optional[ExchangeRates] = None
        self.update_lock = threading.Lock()
        self.supported_currencies = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CNY': '¥',
            'CAD': 'C$',
            'AUD': 'A$',
            'CHF': 'CHF',
            'SEK': 'kr',
            'NOK': 'kr',
            'DKK': 'kr',
            'KRW': '₩',
            'INR': '₹',
            'BRL': 'R$',
            'MXN': '$',
            'RUB': '₽',
            'SGD': 'S$',
            'HKD': 'HK$',
            'NZD': 'NZ$',
            'ZAR': 'R'
        }
    
    def get_currency_symbol(self, currency_code: str) -> str:
        """Get currency symbol for a currency code."""
        return self.supported_currencies.get(
            currency_code.upper(), currency_code.upper()
        )
    
    def get_supported_currencies(self) -> Dict[str, str]:
        """Get all supported currencies with their symbols."""
        return self.supported_currencies.copy()
    
    def update_exchange_rates(self) -> bool:
        """Update exchange rates from API."""
        try:
            # Using exchangerate-api.com (free tier allows 1500 requests/month)
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rates = data.get('rates', {})
            
            with self.update_lock:
                self.exchange_rates = ExchangeRates(
                    rates=rates,
                    last_updated=datetime.now()
                )
            
            logger.info(f"Updated exchange rates: {len(rates)} currencies")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update exchange rates: {e}")
            return False
    
    def convert_price(self, usd_price: float,
                      target_currency: str) -> Optional[float]:
        """Convert USD price to target currency."""
        if target_currency.upper() == 'USD':
            return usd_price

        # Check if we need to update rates
        if (self.exchange_rates is None or
                self.exchange_rates.is_expired()):
            self.update_exchange_rates()

        if self.exchange_rates is None:
            return None

        rate = self.exchange_rates.rates.get(target_currency.upper())
        if rate is None:
            return None

        return usd_price * rate

    def format_price(self, usd_price: float, target_currency: str,
                     decimal_places: int = 4) -> str:
        """Format price in target currency with appropriate symbol."""
        if usd_price <= 0:
            return ''
        
        converted_price = self.convert_price(usd_price, target_currency)
        if converted_price is None:
            return f"${usd_price:.{decimal_places}f}"  # Fallback to USD
        
        symbol = self.get_currency_symbol(target_currency)
        
        # Adjust decimal places based on currency
        if target_currency.upper() in ['JPY', 'KRW']:
            # No decimals for these currencies
            decimal_places = 0
        elif target_currency.upper() in ['EUR', 'GBP', 'USD', 'CAD', 'AUD']:
            # Standard 4 decimals for major currencies
            decimal_places = min(decimal_places, 4)
        
        return f"{symbol}{converted_price:.{decimal_places}f}"
    
    def get_rate_info(self) -> str:
        """Get info about current exchange rates."""
        if self.exchange_rates is None:
            return "Exchange rates not loaded"
        
        time_since_update = datetime.now() - self.exchange_rates.last_updated
        age_minutes = time_since_update.total_seconds() / 60
        num_currencies = len(self.exchange_rates.rates)
        return (f"Rates updated {age_minutes:.0f} min ago "
                f"({num_currencies} currencies)")


# Global converter instance
currency_converter = CurrencyConverter()