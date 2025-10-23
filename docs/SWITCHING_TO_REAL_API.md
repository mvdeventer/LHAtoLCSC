# Switching from Mock Server to Real LCSC API

## Overview

Your application is currently configured to use a mock server at `http://localhost:5000` for testing. Once you receive your LCSC API credentials, you can switch to the real LCSC API by updating your configuration.

## Steps to Switch to Real LCSC API

### 1. Get Your LCSC API Credentials

Contact LCSC to obtain:
- **API Key** (e.g., `your_actual_api_key_here`)
- **API Secret** (e.g., `your_actual_api_secret_here`)

### 2. Update Configuration

You have two options to configure the credentials:

#### Option A: Using the GUI (Recommended)

1. Run the application:
   ```powershell
   python main.py
   ```

2. The application will either:
   - Show a **Setup Wizard** on first run, OR
   - Go to **File → Settings** in the main window

3. In the settings dialog:
   - Enter your **LCSC API Key**
   - Enter your **LCSC API Secret**
   - The **API URL** is already set to `https://api.lcsc.com/v1` (production)
   - Click **Save** or **Test Connection** to verify

4. The settings are automatically saved to a `.env` file

#### Option B: Manually Edit .env File

1. Create or edit the `.env` file in the project root:
   ```
   C:\Projects\LCSC_API\.env
   ```

2. Add your credentials:
   ```env
   # LCSC API Credentials
   LCSC_API_KEY=your_actual_api_key_here
   LCSC_API_SECRET=your_actual_api_secret_here
   
   # API URLs (these are the defaults - no need to change)
   LCSC_API_URL=https://api.lcsc.com/v1
   LCSC_API_BASE_URL=https://www.lcsc.com
   
   # Optional: Network settings
   REQUEST_TIMEOUT=30
   LCSC_API_TIMEOUT=30
   LCSC_API_MAX_RETRIES=3
   ```

3. Save the file

### 3. How the Application Uses Credentials

The application automatically detects which API to use:

```python
# In src/lhatolcsc/core/config.py
self.lcsc_api_base_url = os.getenv("LCSC_API_BASE_URL", "https://www.lcsc.com")
```

**Mock Server Mode** (Current):
- When credentials are set to mock values:
  - `LCSC_API_KEY=test_api_key_12345`
  - `LCSC_API_SECRET=test_api_secret_67890`
  - `LCSC_API_BASE_URL=http://localhost:5000`
- Application connects to local mock server
- Uses local SQLite database with 104,042 products

**Production Mode** (After setup):
- When you enter real LCSC credentials
- Application connects to `https://api.lcsc.com/v1`
- Uses real LCSC inventory and pricing
- Has access to millions of components

### 4. Using the Stock Browser

The **Stock Browser** window automatically adapts:

**Current (Mock Server):**
```python
# Application creates LCSCClient with mock credentials
api_client = LCSCClient(
    api_key="test_api_key_12345",
    api_secret="test_api_secret_67890",
    base_url="http://localhost:5000"  # Mock server
)
```

**After Setup (Real API):**
```python
# Application creates LCSCClient with your credentials
api_client = LCSCClient(
    api_key="your_actual_api_key_here",
    api_secret="your_actual_api_secret_here",
    base_url="https://api.lcsc.com/v1"  # Real API
)
```

**No code changes needed!** The `StockBrowserWindow` uses the same `LCSCClient` for both modes.

### 5. Accessing the Stock Browser

Once configured with real credentials:

1. Run the main application:
   ```powershell
   python main.py
   ```

2. In the main window, go to **Tools → Browse Stock** (or similar menu item)

3. The Stock Browser will now:
   - Search real LCSC inventory
   - Show real-time stock levels
   - Display actual pricing
   - Have access to categories from LCSC

### 6. Testing the Connection

To verify your credentials are working:

1. Open the application
2. Go to **File → Settings**
3. Click **Test Connection** button
4. If successful, you'll see: "✓ Connection successful"
5. If failed, check your credentials

### 7. Differences Between Mock and Production

| Feature | Mock Server | Real LCSC API |
|---------|-------------|---------------|
| **Products** | 104,042 components | Millions of components |
| **Categories** | 3 main (Resistors, Capacitors, ICs) | Full LCSC catalog |
| **Pricing** | Static test data | Real-time pricing |
| **Stock** | Fixed quantities | Live inventory |
| **Search** | Local SQLite (0.6-1.3s) | LCSC servers |
| **Images** | Limited | Full product images |
| **Parameters** | Basic | Complete specifications |

### 8. Important Notes

⚠️ **API Rate Limits:**
- Real LCSC API has rate limits
- Avoid excessive rapid requests
- Use pagination efficiently

⚠️ **Network Requirements:**
- Need internet connection for real API
- Mock server works offline

⚠️ **Credentials Security:**
- Never commit `.env` file to git
- `.env` is already in `.gitignore`
- Keep your API secret secure

### 9. Switching Back to Mock Server

If you want to test with the mock server again:

1. Stop any running application
2. Start the mock server:
   ```powershell
   .\start_mock_server.ps1
   ```
3. Update `.env` to use mock credentials:
   ```env
   LCSC_API_KEY=test_api_key_12345
   LCSC_API_SECRET=test_api_secret_67890
   LCSC_API_BASE_URL=http://localhost:5000
   ```
4. Restart the application

### 10. Troubleshooting

**Problem: "Connection failed" error**
- Check internet connection
- Verify credentials are correct
- Check LCSC API status

**Problem: "Authentication failed" (401)**
- Credentials are incorrect
- API key/secret don't match
- Check for typos in `.env` file

**Problem: Categories not showing**
- Mock server: Categories assigned based on keywords
- Real API: Categories come from LCSC
- May need to refresh/reload

**Problem: Slow searches**
- Real API depends on internet speed
- Use specific search terms
- Reduce page size if needed

## Summary

**Current State:**
- Using mock server at `localhost:5000`
- 104,042 test products in SQLite database
- Categories auto-assigned from keywords

**After LCSC Credentials:**
- Change 2 lines in `.env` file (or use Settings GUI)
- Application automatically connects to real LCSC API
- Stock Browser shows real inventory
- No code changes required!

The application is designed to seamlessly work with both mock and production APIs using the same interface.
