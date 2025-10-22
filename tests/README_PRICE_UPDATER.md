# Mock Database Price & Stock Updater

This tool updates your mock database with realistic pricing tiers and stock quantities.

## Two Modes

### 1. Default Patterns (Recommended for Testing)
Uses realistic pricing patterns based on typical LCSC pricing:
- **Resistors**: $0.0012 base, 50K-500K stock
- **Capacitors**: $0.015 base, 30K-300K stock  
- **ICs**: $1.50 base, 1K-50K stock
- **Connectors**: $0.25 base, 5K-100K stock

**Usage:**
```bash
cd tests
python update_mock_with_real_data.py
```

### 2. Real LCSC API (For Production-Like Data)
Queries the real LCSC API to get actual pricing from real products, then applies variations.

**Requirements:**
- Valid LCSC API credentials in `.env` file
- API credits available

**Usage:**
```bash
cd tests
python update_mock_with_real_data.py --real-api
```

## What It Does

1. **Reads** `mock_products_large.json` (104,042 products)
2. **Categorizes** each product (resistor/capacitor/IC/connector)
3. **Generates** realistic pricing with 5 tiers per product:
   - Example: 1+, 10+, 100+, 500+, 1000+
   - Volume discounts: 10-30% off for bulk
4. **Generates** realistic stock quantities:
   - Resistors/Caps: High stock (50K-500K)
   - ICs: Moderate stock (1K-50K)
   - Connectors: Variable stock (5K-100K)
5. **Updates** the file in-place
6. **Shows** a sample product with new pricing

## Example Output

```
Sample Product (after update):
================================================================================
Code: C100000
Name: RES 0.1Ω ±0.1% 1/16W 0201 ±25ppm
Stock: 276,543
Price Tiers:
      1+: $0.0014
     10+: $0.0013
    100+: $0.0011
    500+: $0.0010
   1000+: $0.0010
```

## After Running

1. **Stop** the mock server (if running)
2. **Restart** the mock server to load new prices:
   ```bash
   python tests\mock_lcsc_server.py
   ```
3. **Test** in stock browser - you'll see:
   - Varied stock quantities
   - Realistic price tiers
   - Volume discounts

## Querying Real LCSC API

If you choose `--real-api` mode, the script will:

1. Query these real LCSC product codes:
   ```python
   C17572   # 10K resistor
   C25804   # 100K resistor
   C22790   # 1K resistor
   C15849   # 100nF capacitor
   C14663   # 10uF capacitor
   C1525    # 1uF capacitor
   C2040    # STM32 MCU
   C72041   # Red LED
   C81598   # 1N4148 diode
   C20917   # N-channel MOSFET
   C5446    # LM358 op-amp
   C9002    # 8MHz crystal
   ```

2. Extract their real pricing structures
3. Apply those patterns to similar products in your mock database
4. Add ±5-20% variation for diversity

## Benefits

- **Realistic Testing**: Prices and quantities match real-world scenarios
- **Better Demos**: Show realistic volume discounts
- **Stock Sorting**: Test low-stock vs high-stock scenarios
- **Price Sorting**: Verify price comparison features work correctly

## Safety

- Creates backup: The original file is overwritten, so back it up first if needed
- No API calls in default mode: Safe to run without LCSC credentials
- Rate limited: When using real API, waits 0.5s between requests
