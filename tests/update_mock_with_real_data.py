"""
Update mock database with real pricing and stock data from LCSC API.

This script:
1. Queries the real LCSC API for a sample of products
2. Extracts their real pricing tiers and stock quantities
3. Uses that data to update the mock database with realistic values
"""

import json
import random
import time
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path so we can import lhatolcsc
sys.path.insert(0, str(Path(__file__).parent.parent))

from lhatolcsc.api.client import LCSCClient
from lhatolcsc.core.config import Config

# Real LCSC product codes to sample (these are real parts)
SAMPLE_PRODUCT_CODES = [
    "C17572",  # 10K resistor
    "C25804",  # 100K resistor
    "C22790",  # 1K resistor
    "C15849",  # 100nF capacitor
    "C14663",  # 10uF capacitor
    "C1525",   # 1uF capacitor
    "C2040",   # STM32 MCU
    "C72041",  # Red LED
    "C81598",  # 1N4148 diode
    "C20917",  # N-channel MOSFET
    "C5446",   # LM358 op-amp
    "C9002",   # 8MHz crystal
]

def get_real_pricing_patterns(config: Config) -> List[Dict[str, Any]]:
    """
    Query real LCSC API to get pricing patterns.
    
    Returns:
        List of pricing pattern dictionaries with real data
    """
    print("Connecting to real LCSC API...")
    
    if not config.is_configured():
        print("⚠️  WARNING: LCSC API credentials not configured in .env file")
        print("   Using default pricing patterns instead of real API data")
        return get_default_pricing_patterns()
    
    client = LCSCClient(
        api_key=config.lcsc_api_key,
        api_secret=config.lcsc_api_secret,
        base_url=config.lcsc_api_base_url
    )
    
    pricing_patterns = []
    
    for product_code in SAMPLE_PRODUCT_CODES:
        try:
            print(f"  Fetching {product_code}...")
            product = client.get_product_details(product_code)
            
            if product and product.price_tiers:
                pattern = {
                    'product_code': product_code,
                    'product_name': product.product_name,
                    'stock': product.stock,
                    'price_tiers': [
                        {
                            'quantity': tier.quantity,
                            'unit_price': tier.unit_price
                        }
                        for tier in product.price_tiers
                    ]
                }
                pricing_patterns.append(pattern)
                print(f"    ✓ Got {len(product.price_tiers)} price tiers, stock: {product.stock}")
            
            # Rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"    ✗ Error fetching {product_code}: {e}")
            continue
    
    if not pricing_patterns:
        print("⚠️  No real data retrieved, using default patterns")
        return get_default_pricing_patterns()
    
    print(f"\n✓ Retrieved {len(pricing_patterns)} real pricing patterns from LCSC API")
    return pricing_patterns


def get_default_pricing_patterns() -> List[Dict[str, Any]]:
    """
    Default pricing patterns based on typical LCSC pricing.
    Used as fallback when API is not available.
    
    All possible price break quantities up to 10000:
    [1, 10, 25, 50, 100, 200, 500, 1000, 5000, 10000]
    
    Each component will randomly get 1-10 of these price breaks.
    """
    # All possible LCSC price break quantities (up to 10000, can be extended)
    ALL_PRICE_BREAKS = [
        {'quantity': 1, 'multiplier': 1.0},
        {'quantity': 10, 'multiplier': 0.90},
        {'quantity': 25, 'multiplier': 0.85},
        {'quantity': 50, 'multiplier': 0.82},
        {'quantity': 100, 'multiplier': 0.78},
        {'quantity': 200, 'multiplier': 0.75},
        {'quantity': 500, 'multiplier': 0.72},
        {'quantity': 1000, 'multiplier': 0.70},
        {'quantity': 5000, 'multiplier': 0.68},
        {'quantity': 10000, 'multiplier': 0.65},
    ]
    
    return [
        # Resistors - very cheap, very high stock
        {
            'category': 'resistor',
            'base_price': 0.0012,
            'stock_range': (100000, 800000),
            'all_price_tiers': ALL_PRICE_BREAKS,
        },
        # Capacitors - cheap, high stock
        {
            'category': 'capacitor',
            'base_price': 0.015,
            'stock_range': (50000, 500000),
            'all_price_tiers': ALL_PRICE_BREAKS,
        },
        # Inductors - moderate price, moderate stock
        {
            'category': 'inductor',
            'base_price': 0.08,
            'stock_range': (20000, 200000),
            'all_price_tiers': ALL_PRICE_BREAKS,
        },
        # Crystals - moderate price, lower stock
        {
            'category': 'crystal',
            'base_price': 0.12,
            'stock_range': (10000, 100000),
            'all_price_tiers': ALL_PRICE_BREAKS,
        },
        # ICs - higher price, lower stock
        {
            'category': 'ic',
            'base_price': 1.50,
            'stock_range': (2000, 50000),
            'all_price_tiers': ALL_PRICE_BREAKS,
        },
        # Sensors - higher price, low stock
        {
            'category': 'sensor',
            'base_price': 2.50,
            'stock_range': (1000, 30000),
            'all_price_tiers': ALL_PRICE_BREAKS,
        },
        # Connectors - moderate price, varied stock
        {
            'category': 'connector',
            'base_price': 0.25,
            'stock_range': (5000, 150000),
            'all_price_tiers': ALL_PRICE_BREAKS,
        },
    ]


def categorize_product(product: Dict[str, Any]) -> str:
    """Determine product category from name."""
    name = product.get('productName', '').upper()
    
    if 'RES' in name or 'RESISTOR' in name:
        return 'resistor'
    elif 'CAP' in name or 'CAPACITOR' in name:
        return 'capacitor'
    elif 'IND' in name or 'INDUCTOR' in name:
        return 'inductor'
    elif 'CRYSTAL' in name or 'OSCILLATOR' in name:
        return 'crystal'
    elif 'MCU' in name or 'MICROCONTROLLER' in name or 'IC' in name or 'OP-AMP' in name or 'OPAMP' in name or 'REGULATOR' in name:
        return 'ic'
    elif 'SENSOR' in name or 'TEMP' in name or 'PRESSURE' in name or 'HUMIDITY' in name:
        return 'sensor'
    elif 'CONNECTOR' in name or 'HEADER' in name or 'USB' in name or 'CARD' in name or 'TERMINAL' in name:
        return 'connector'
    else:
        return 'capacitor'  # Default


def generate_realistic_pricing(category: str, patterns: List[Dict[str, Any]]) -> tuple:
    """
    Generate realistic pricing and stock based on category and real patterns.
    
    Returns:
        (stock_number, price_list)
    """
    # Find pattern for this category
    pattern = None
    for p in patterns:
        if isinstance(p, dict) and p.get('category') == category:
            pattern = p
            break
    
    if not pattern:
        # Use first pattern as default
        pattern = patterns[0] if patterns else get_default_pricing_patterns()[0]
    
    # Generate stock
    if 'stock_range' in pattern:
        stock = random.randint(*pattern['stock_range'])
    else:
        # Based on real data
        stock = random.randint(10000, 100000)
    
    # Generate prices
    price_list = []
    
    if 'all_price_tiers' in pattern:
        # NEW: Randomly select 1-10 price breaks from all available tiers
        all_tiers = pattern['all_price_tiers']
        num_tiers = random.randint(1, min(10, len(all_tiers)))
        
        # Always include tier 1, then randomly select others
        selected_tiers = [all_tiers[0]]  # Always include qty 1
        if num_tiers > 1:
            # Randomly select additional tiers (without replacement)
            remaining_tiers = all_tiers[1:]
            additional = random.sample(remaining_tiers, min(num_tiers - 1, len(remaining_tiers)))
            selected_tiers.extend(additional)
        
        # Sort by quantity to keep them in order
        selected_tiers.sort(key=lambda x: x['quantity'])
        
        # Generate prices based on selected tiers
        base_price = pattern['base_price'] * random.uniform(0.8, 1.5)
        
        for tier in selected_tiers:
            price_list.append({
                'startAmount': tier['quantity'],
                'endAmount': 999999,
                'productPrice': round(base_price * tier['multiplier'], 4),
                'currencySymbol': 'US$',
                'currencyCode': 'USD'
            })
    elif 'base_price' in pattern and 'price_tiers' in pattern:
        # Using pattern-based pricing (old format)
        base_price = pattern['base_price'] * random.uniform(0.8, 1.5)
        
        for tier in pattern['price_tiers']:
            price_list.append({
                'startAmount': tier['quantity'],
                'endAmount': 999999,
                'productPrice': round(base_price * tier['multiplier'], 4),
                'currencySymbol': 'US$',
                'currencyCode': 'USD'
            })
    else:
        # Using real API data
        base_price = pattern['price_tiers'][0]['unit_price'] * random.uniform(0.9, 1.2)
        
        for tier in pattern['price_tiers']:
            # Scale the real prices slightly for variety
            scaled_price = tier['unit_price'] * random.uniform(0.95, 1.05)
            price_list.append({
                'startAmount': tier['quantity'],
                'endAmount': 999999,
                'productPrice': round(scaled_price, 4),
                'currencySymbol': 'US$',
                'currencyCode': 'USD'
            })
    
    return stock, price_list


def update_mock_database(input_file: str, output_file: str, use_real_api: bool = True):
    """
    Update mock database with realistic pricing and stock.
    
    Args:
        input_file: Path to current mock database
        output_file: Path to save updated database
        use_real_api: Whether to query real LCSC API for pricing patterns
    """
    print("=" * 80)
    print("Mock Database Price & Stock Updater")
    print("=" * 80)
    
    # Get pricing patterns
    if use_real_api:
        config = Config()
        patterns = get_real_pricing_patterns(config)
    else:
        print("Using default pricing patterns (not querying real API)")
        patterns = get_default_pricing_patterns()
    
    # Load mock database
    print(f"\nLoading mock database from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Loaded {len(products)} products")
    
    # Update each product
    print("\nUpdating products with realistic pricing, stock, and images...")
    updated_count = 0
    
    # Generic component images by category
    image_urls = {
        'resistor': 'https://wmsc.lcsc.com/szlcsc/2304140030_UNI-ROYAL-Uniroyal-Elec-0402WGF1000TCE_C25744.jpg',
        'capacitor': 'https://wmsc.lcsc.com/szlcsc/1811151211_Samsung-Electro-Mechanics-CL10A106KP8NNNC_C15849.jpg',
        'inductor': 'https://wmsc.lcsc.com/szlcsc/2205251630_Sunlord-SDWL1608C1N0SSTFR_C5142046.jpg',
        'crystal': 'https://wmsc.lcsc.com/szlcsc/1810311810_Seiko-Epson-Q13FC1350000400_C32346.jpg',
        'ic': 'https://wmsc.lcsc.com/szlcsc/1811151232_STMicroelectronics-STM32F103C8T6_C8734.jpg',
        'sensor': 'https://wmsc.lcsc.com/szlcsc/1912111437_Sensirion-SHT31-DIS-B_C111093.jpg',
        'connector': 'https://wmsc.lcsc.com/szlcsc/1912111437_SOFNG-C264553_C264553.jpg',
    }
    
    for code, product in products.items():
        category = categorize_product(product)
        stock, price_list = generate_realistic_pricing(category, patterns)
        
        # Update product with pricing, stock, image, and datasheet URL
        product['stockNumber'] = stock
        product['productPriceList'] = price_list
        product['productImages'] = image_urls.get(category, image_urls['capacitor'])  # Default to capacitor image
        
        # Add datasheet URL using LCSC API format
        product_code = product.get('productCode', code)
        if product_code:
            # LCSC datasheet URL format: https://www.lcsc.com/datasheet/[productCode].pdf
            product['pdfUrl'] = f"https://www.lcsc.com/datasheet/lcsc_datasheet_{product_code}.pdf"
        
        updated_count += 1
        
        if updated_count % 10000 == 0:
            print(f"  Updated {updated_count}/{len(products)} products...")
    
    print(f"✓ Updated all {updated_count} products with pricing, stock, images, and datasheets")
    
    # Save updated database
    print(f"\nSaving updated database to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    file_size_mb = len(json.dumps(products, ensure_ascii=False)) / 1024 / 1024
    print(f"✓ Saved successfully ({file_size_mb:.2f} MB)")
    
    # Show sample
    print("\n" + "=" * 80)
    print("Sample Product (after update):")
    print("=" * 80)
    sample = list(products.values())[0]
    print(f"Code: {sample['productCode']}")
    print(f"Name: {sample['productName']}")
    print(f"Stock: {sample['stockNumber']:,}")
    print(f"Price Tiers:")
    for tier in sample['productPriceList']:
        print(f"  {tier['startAmount']:>5}+: ${tier['productPrice']:.4f}")
    
    print("\n" + "=" * 80)
    print("Update completed successfully!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Restart your mock server to load the new pricing")
    print("2. Test the stock browser to see realistic prices and quantities")
    print("3. Use the real API flag to update with actual LCSC pricing periodically")


if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    use_real_api = '--real-api' in sys.argv or '-r' in sys.argv
    
    # File paths
    input_file = 'mock_products_large.json'
    output_file = 'mock_products_large.json'  # Overwrite
    
    print("\nOptions:")
    print(f"  Use real LCSC API: {use_real_api}")
    print(f"  Input file: {input_file}")
    print(f"  Output file: {output_file}")
    
    if use_real_api:
        print("\n⚠️  This will query the real LCSC API")
        print("   Make sure you have valid credentials in .env file")
        response = input("\nContinue? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)
    
    update_mock_database(input_file, output_file, use_real_api)
