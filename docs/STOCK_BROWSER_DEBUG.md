# Stock Browser Debug Tool

## Overview

The Stock Browser is a debug tool that allows you to browse and search the mock server's component inventory directly from the application GUI.

## Features

- **Scrollable Table View**: Browse through 104,042+ components with smooth scrolling
- **Search/Filter**: Search by keyword to find specific components
- **Pagination**: Navigate through results with configurable page sizes (50, 100, 200, 500)
- **Detailed View**: Double-click any product to see full details including:
  - Product code and number
  - Manufacturer and MPN
  - Category and package type
  - Stock availability
  - Pricing tiers
  - Description
  - Datasheet links
- **CSV Export**: Export visible results to CSV file with timestamp
- **Real-time Updates**: Refresh button to reload data from mock server

## How to Use

### 1. Start the Mock Server

Before using the stock browser, ensure the mock server is running:

```powershell
C:/Projects/LCSC_API/venv/Scripts/python.exe tests\mock_lcsc_server.py
```

The server will start on `http://localhost:5000` with 104,042 components.

Mock credentials:
- API Key: `test_api_key_12345`
- API Secret: `test_api_secret_67890`

### 2. Configure API Settings

1. Run the application: `python main.py`
2. Go to `File → Settings`
3. Click "Fill Mock Server Credentials" button
4. This auto-fills:
   - API URL: http://localhost:5000
   - API Key: test_api_key_12345
   - API Secret: test_api_secret_67890
5. Click "Test Connection" to verify
6. Click "Save" to store settings

### 3. Open Stock Browser

1. From main window, go to `Tools → Browse Mock Server Stock (Debug)`
2. The stock browser window will open
3. Products will automatically load on first open

### 4. Browse Products

The table displays:
- **Product Code**: LCSC part number (e.g., C100000)
- **Model**: Manufacturer part number/model
- **Name**: Product name/description
- **Brand**: Manufacturer brand
- **Package**: Package type (0402, 0603, SOT-23, etc.)
- **Stock**: Available quantity
- **Price (1+)**: Unit price for 1 piece
- **Price (10+)**: Unit price for 10 pieces
- **Price (100+)**: Unit price for 100 pieces

### 5. Search Components

1. Enter search keyword in the search field (e.g., "resistor", "capacitor", "STM32")
2. Press Enter or click "Search"
3. Results will update with matching components
4. Click "Clear" to reset and show all products

### 6. Navigate Pages

- Use "◀ Previous" and "Next ▶" buttons to navigate
- Change page size (50/100/200/500) from dropdown
- Page info shows current page and total pages
- Status bar shows how many products are loaded

### 7. View Details

1. Double-click any row in the table
2. A detailed view window opens showing:
   - Complete product information
   - Full pricing tiers
   - Description
   - Datasheet URL (if available)
   - Image URL (if available)
3. Scroll through details if content is long
4. Click "Close" to return to browser

### 8. Export to CSV

1. Click "Export to CSV" button
2. Choose save location and filename
3. All currently visible products will be exported
4. Default filename includes timestamp: `mock_server_stock_YYYYMMDD_HHMMSS.csv`
5. CSV includes all product details and pricing

## Database Contents

The mock server includes:

### Large Database (104,042 components):
- **Resistors**: C100000 - C125041 (25,042 components)
  - Values: 1Ω to 10MΩ
  - Packages: 0402, 0603, 0805, 1206
  - Tolerances: 1%, 5%
  - Power ratings: 1/16W to 1/4W
  
- **Capacitors**: C125042 - C150083 (25,042 components)
  - Values: 1pF to 100µF
  - Packages: 0402, 0603, 0805, 1206
  - Types: Ceramic (X7R, X5R, C0G)
  - Voltages: 16V, 25V, 50V
  
- **Inductors**: C150084 - C175125 (25,042 components)
  - Values: 1nH to 1mH
  - Packages: 0402, 0603, 0805, 1206
  - Types: Chip inductors, power inductors
  
- **Crystals**: C175126 - C179125 (4,000 components)
  - Frequencies: 4MHz to 50MHz
  - Packages: SMD-3225, SMD-5032
  - Types: Crystal oscillators, resonators

- **Integrated Circuits**: C179126 - C189125 (10,000 ICs)
  - Microcontrollers (STM32, AVR, ESP32)
  - Op-Amps (TL071, LM358, OPA series)
  - Voltage Regulators (LM7805, AMS1117, etc.)
  - Logic ICs (74HC series, CD4000 series)
  - Interface ICs (RS485, CAN, I2C)

- **Sensors**: C189126 - C194125 (5,000 sensors)
  - Temperature (DS18B20, LM35, DHT22)
  - Pressure (BMP280, MPX series)
  - Motion (MPU6050, ADXL345)
  - Light (TSL2561, BH1750)

- **Connectors**: C194126 - C204041 (9,916 connectors)
  - Headers (pin headers, socket headers)
  - USB (Type-A, Type-C, Micro-USB)
  - Terminal blocks
  - JST connectors
  - D-Sub connectors

### Quick Test Database (25 components):
- Pre-selected common components for quick testing
- See mock server startup output for full list

## Technical Details

### API Client Integration
- Uses `LCSCClient.search_products()` method
- Returns `SearchResult` dataclass with `LCSCProduct` objects
- Handles pagination automatically
- Supports keyword search and filtering

### Performance
- Pagination limits data transfer (default 100 products per page)
- Adjustable page sizes for different use cases
- Smooth scrolling with native Tkinter Treeview
- Minimal memory footprint

### Error Handling
- Checks if API client is configured before opening
- Displays warnings if mock server is not running
- Graceful error messages for connection failures
- Logs all errors for debugging

## Troubleshooting

### "API Not Configured" Error
- Go to File → Settings
- Click "Fill Mock Server Credentials"
- Click "Test Connection" to verify
- Save settings

### "Failed to load products" Error
- Ensure mock server is running: `python tests\mock_lcsc_server.py`
- Check that server is on http://localhost:5000
- Verify API credentials are correct
- Check terminal output for server errors

### Empty Results
- Click "Refresh" to reload data
- Try clearing search filter with "Clear" button
- Check mock server terminal for request logs

### Slow Performance
- Reduce page size to 50 or 100 products
- Close and reopen browser window to reset state
- Check if mock server is responding (server should log requests)

## Future Enhancements

Possible improvements for future versions:
- Filter by category (resistors, capacitors, etc.)
- Filter by brand/manufacturer
- Filter by package type
- Advanced search (price range, stock availability)
- Sort by column headers (ascending/descending)
- Multi-column sorting
- Bookmarks/favorites
- Shopping cart/BOM builder
- Bulk operations

## Notes

- This is a **debug tool only** - not intended for production use
- Uses mock server data, not real LCSC inventory
- Designed for testing and development purposes
- Stock numbers and prices are simulated data
- Real LCSC API may have different response formats

## Related Files

- `src/lhatolcsc/gui/stock_browser.py` - Stock browser window implementation
- `src/lhatolcsc/gui/main_window.py` - Main window with menu integration
- `tests/mock_lcsc_server.py` - Mock server with 104k+ components
- `tests/mock_products_large.json` - Product database (102MB, excluded from git)
- `src/lhatolcsc/api/client.py` - LCSC API client
- `src/lhatolcsc/api/models.py` - Data models (LCSCProduct, SearchResult)
