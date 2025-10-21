# Mock LCSC API Server - Testing Guide

## Overview

This mock server simulates the LCSC API for testing your application without needing real API credentials or making actual API calls to LCSC.

## Quick Start

### 1. Install Flask

```powershell
.\venv\Scripts\Activate.ps1
pip install flask
```

Or install from requirements file:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r tests/requirements-mock.txt
```

### 2. Start the Mock Server

Open a **new terminal window** and run:

```powershell
.\venv\Scripts\Activate.ps1
python tests/mock_lcsc_server.py
```

You should see:

```
============================================================
Mock LCSC API Server
============================================================

Server URL: http://localhost:5000

Mock Credentials:
  API Key:    test_api_key_12345
  API Secret: test_api_secret_67890

Available Endpoints:
  GET  /health                                    - Health check
  POST /rest/wmsc2agent/search/product           - Search products
  GET  /rest/wmsc2agent/product/info/<code>      - Get product details
  POST /rest/wmsc2agent/product/batch            - Batch get products
  GET  /rest/wmsc2agent/category                 - Get categories
  GET  /rest/wmsc2agent/brand                    - Get brands
  GET  /api/test/connection                      - Test connection

Mock Products Available:
  C17572: 0603WAF1002T5E - RES 10K OHM 1% 1/10W 0603
  C15849: CL10A475KO8NNNC - CAP CER 4.7UF 16V X5R 0603
  C2040: STM32F103C8T6 - MCU ARM 32BIT 64KB FLASH LQFP48

============================================================
Server starting...
============================================================
```

### 3. Configure Your Application

In the setup wizard or settings dialog, enter:

**API Key:** `test_api_key_12345`  
**API Secret:** `test_api_secret_67890`  
**API Base URL:** `http://localhost:5000`

### 4. Test Your Application

Now run your application in a **different terminal**:

```powershell
.\venv\Scripts\Activate.ps1
python main.py
```

Click **"Test Connection"** in the wizard - it should succeed!

## Mock Credentials

```
API Key:    test_api_key_12345
API Secret: test_api_secret_67890
API URL:    http://localhost:5000
```

## Available Mock Products

The mock server has 3 test products:

### 1. Resistor
- **Product Code:** C17572
- **Model:** 0603WAF1002T5E
- **Description:** RES 10K OHM 1% 1/10W 0603
- **Brand:** UNI-ROYAL(Uniroyal Elec)
- **Package:** 0603
- **Stock:** 125,000 pcs
- **Price:** $0.0005 - $0.0003 (qty dependent)

### 2. Capacitor
- **Product Code:** C15849
- **Model:** CL10A475KO8NNNC
- **Description:** CAP CER 4.7UF 16V X5R 0603
- **Brand:** SAMSUNG
- **Package:** 0603
- **Stock:** 89,500 pcs
- **Price:** $0.0234 - $0.0154 (qty dependent)

### 3. Microcontroller
- **Product Code:** C2040
- **Model:** STM32F103C8T6
- **Description:** MCU ARM 32BIT 64KB FLASH LQFP48
- **Brand:** STMicroelectronics
- **Package:** LQFP-48
- **Stock:** 5,420 pcs
- **Price:** $2.85 - $1.98 (qty dependent)

## Testing Scenarios

### Test Product Search

Search for these terms to get results:
- "10K" → Returns resistor (C17572)
- "4.7UF" → Returns capacitor (C15849)
- "STM32" → Returns microcontroller (C2040)
- "0603" → Returns both resistor and capacitor
- "C17572" → Returns resistor by product code

### Test Product Details

Get details for specific products:
- Product Code: C17572
- Product Code: C15849
- Product Code: C2040

### Test Connection

Use the "Test Connection" button in your application to verify:
- Authentication works
- Network connectivity is good
- Server is responding

## API Endpoints

### Health Check
```
GET http://localhost:5000/health
```

### Search Products
```
POST http://localhost:5000/rest/wmsc2agent/search/product?key=test_api_key_12345&timestamp=1234567890&nonce=abc123&signature=YOUR_SIG
Body: {
  "keyword": "10K",
  "current_page": 1,
  "page_size": 10
}
```

Or using GET with query params:
```
GET http://localhost:5000/rest/wmsc2agent/search/product?keyword=10K&current_page=1&page_size=10&key=test_api_key_12345&timestamp=1234567890&nonce=abc123&signature=YOUR_SIG
```

### Get Product Detail
```
GET http://localhost:5000/rest/wmsc2agent/product/info/C17572?key=test_api_key_12345&timestamp=1234567890&nonce=abc123&signature=YOUR_SIG
```

### Get Categories
```
GET http://localhost:5000/rest/wmsc2agent/category?key=test_api_key_12345&timestamp=1234567890&nonce=abc123&signature=YOUR_SIG
```

### Get Brands
```
GET http://localhost:5000/rest/wmsc2agent/brand?key=test_api_key_12345&timestamp=1234567890&nonce=abc123&signature=YOUR_SIG
```

### Test Connection (Simplified)
```
GET http://localhost:5000/api/test/connection?key=test_api_key_12345
```

## Response Format

All responses follow this format:

```json
{
  "success": true,
  "code": 200,
  "message": "Success",
  "result": {
    // ... result data
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "code": 401,
  "message": "Invalid API key",
  "result": null
}
```

## Authentication

The mock server requires authentication via **query parameters** (matching real LCSC API):

- `key`: API Key (required) - Use `test_api_key_12345`
- `timestamp`: Unix timestamp (required)
- `nonce`: Random string (required)
- `signature`: SHA1 signature (required) - Generated from key+secret+timestamp+nonce

**For simplified testing**, the mock server accepts any signature as long as:
1. The `key` parameter matches `test_api_key_12345`
2. All required parameters (key, timestamp, nonce, signature) are present

In production with real LCSC API, the signature must be correctly calculated using SHA1.

## Troubleshooting

### Server Won't Start

**Error:** `ModuleNotFoundError: No module named 'flask'`  
**Solution:** Install Flask:
```powershell
.\venv\Scripts\Activate.ps1
pip install flask
```

**Error:** `Address already in use`  
**Solution:** Another process is using port 5000. Either:
1. Stop the other process
2. Or change port in `mock_lcsc_server.py` (line 307):
   ```python
   app.run(host='0.0.0.0', port=5001, debug=True)
   ```

### Application Can't Connect

**Issue:** "Connection Failed" in application  
**Check:**
1. Mock server is running (check terminal)
2. API URL is `http://localhost:5000` (not https)
3. API Key is `test_api_key_12345`
4. No firewall blocking port 5000

### No Products Found

**Issue:** Search returns empty results  
**Remember:** Only 3 products available. Search for:
- "10K", "0603WAF1002T5E", or "C17572"
- "4.7UF", "CL10A475KO8NNNC", or "C15849"
- "STM32", "STM32F103C8T6", or "C2040"

## Adding More Mock Products

Edit `tests/mock_lcsc_server.py` and add to `MOCK_PRODUCTS` dictionary:

```python
MOCK_PRODUCTS = {
    "C12345": {
        "productCode": "C12345",
        "productModel": "YOUR_MODEL_NUMBER",
        "productName": "YOUR PRODUCT NAME",
        "brandName": "YOUR BRAND",
        "packageType": "0402",
        "productUnit": "pcs",
        "minPacketUnit": "1000",
        "minBuyNumber": "1",
        "stockNumber": "50000",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0010", "discountRate": "100"}
        ],
        "paramVOList": []
    }
}
```

Restart the server to see changes.

## Workflow for Testing

1. **Terminal 1:** Start mock server
   ```powershell
   .\venv\Scripts\Activate.ps1
   python tests/mock_lcsc_server.py
   ```

2. **Terminal 2:** Run your application
   ```powershell
   .\venv\Scripts\Activate.ps1
   python main.py
   ```

3. **In Application:**
   - Enter mock credentials
   - Test connection ✅
   - Save settings
   - Test BOM matching with mock products

## Switching Back to Real API

When ready to use real LCSC API:

1. Stop the mock server (Ctrl+C in Terminal 1)
2. Open application
3. Go to **Tools > Settings**
4. Change:
   - API Key: `<your real key>`
   - API Secret: `<your real secret>`
   - API Base URL: `https://api.lcsc.com/v1`
5. Test connection with real credentials
6. Save

## Benefits of Mock Server

✅ **No Real API Needed:** Test without LCSC account  
✅ **Fast Development:** No network delays  
✅ **Offline Testing:** Works without internet  
✅ **Predictable Results:** Same data every time  
✅ **No Rate Limits:** Test as much as you want  
✅ **Free:** No API costs  
✅ **Safe:** Can't accidentally place real orders  

## Notes

- Mock server runs on `localhost` only (not accessible from other machines)
- Data is stored in memory (resets when server restarts)
- Simplified authentication (real LCSC API uses SHA1 signatures)
- Limited product database (3 products vs thousands in real API)
- No actual order processing
- Perfect for development and testing!

---

**Ready to test your application? Start the mock server and enter the credentials! 🚀**
