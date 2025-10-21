# LHAtoLCSC Project Plan

## Project Overview

**Project Name:** LHAtoLCSC  
**Version:** 1.0.0  
**Purpose:** A professional Tkinter-based desktop application to match BOM components with LCSC parts using fuzzy search and API integration.

---

## Executive Summary

LHAtoLCSC is a Python desktop application that bridges the gap between custom Bill of Materials (BOM) Excel files and the LCSC electronic components database. The application enables users to:

1. Load BOM files from Excel
2. Search for components using the "Stock Part Name" column
3. Match components with LCSC parts using fuzzy search
4. Automatically add LCSC part numbers to the BOM
5. Export updated BOM with LCSC part numbers and pricing information

---

## LCSC API Research Summary

### Available APIs

Based on research of LCSC's official API documentation (https://www.lcsc.com/docs/), the following APIs are available:

#### 1. **Category API**
- **Endpoint:** `GET /rest/wmsc2agent/category`
- **Purpose:** Retrieve all item categories and subcategories
- **Use Case:** Browse and filter components by category

#### 2. **Manufacturer API**
- **Endpoint:** `GET /rest/wmsc2agent/brand`
- **Purpose:** Get all manufacturer information
- **Use Case:** Filter searches by manufacturer/brand

#### 3. **Categorical Item List API**
- **Endpoint:** `GET /rest/wmsc2agent/category/product/{category_id}`
- **Purpose:** Get all items in a specific category
- **Parameters:**
  - `category_id` (required)
  - `currency` (USD, EUR, GBP, etc.)
  - `current_page`, `page_size`
  - `is_available` (in-stock only)
  - `is_pre_sale`
  - `user_type`

#### 4. **Item Details API**
- **Endpoint:** `GET /rest/wmsc2agent/product/info/{product_number}`
- **Purpose:** Get detailed information for a specific product
- **Use Case:** Retrieve full specifications, pricing, stock levels

#### 5. **Keyword Search List API** ⭐ **PRIMARY FOR THIS PROJECT**
- **Endpoint:** `GET /rest/wmsc2agent/search/product`
- **Purpose:** Search products by keyword
- **Parameters:**
  - `keyword` (SKU/MPN/Category/Manufacturer)
  - `match_type` (`exact` or `fuzzy`)
  - `current_page`, `page_size` (max 100)
  - `is_available` (in-stock filter)
  - `is_pre_sale`
- **Use Case:** **Core functionality for fuzzy matching BOM parts**

#### 6. **Order Create API**
- **Endpoint:** `POST /rest/wmsc2agent/submit/order`
- **Purpose:** Programmatically create orders
- **Use Case:** Future feature - direct ordering from BOM

#### 7. **Check Order API**
- **Endpoint:** `GET /rest/wmsc2agent/select/order/page`
- **Purpose:** Query order details
- **Use Case:** Track order status

#### 8. **Get Shipment API**
- **Endpoint:** `POST /rest/wmsc2agent/get/shipment`
- **Purpose:** Get shipping methods and costs
- **Use Case:** Calculate shipping for orders

### API Authentication

All LCSC API requests require:

1. **API Key:** `key` - User ID from LCSC account
2. **API Secret:** `secret` - Used for signature generation (not sent in request)
3. **Timestamp:** `timestamp` - Request timestamp (must be within 60 seconds)
4. **Nonce:** `nonce` - 16-character random string
5. **Signature:** `signature` - SHA1 hash of concatenated parameters

**Signature Algorithm:**
```
signature = sha1("key={key}&nonce={nonce}&secret={secret}&timestamp={timestamp}")
```

### API Rate Limits

- **Default:** 1,000 searches/day, 200 searches/minute
- **Higher limits:** Available upon request to support@lcsc.com

### Response Format

```json
{
    "success": true,
    "code": 200,
    "message": "",
    "result": { /* API-specific data */ }
}
```

---

## Technical Architecture

### Technology Stack

- **Language:** Python 3.10+
- **GUI Framework:** Tkinter with ttk (themed widgets)
- **HTTP Client:** `requests` library
- **Excel Processing:** `openpyxl` and `pandas`
- **Fuzzy Matching:** `fuzzywuzzy` or `rapidfuzz`
- **Configuration:** `python-dotenv` for environment variables
- **Logging:** Built-in `logging` module
- **Testing:** `pytest` with `pytest-cov`
- **Code Quality:** `black`, `flake8`, `mypy`

### Project Structure

```
LHAtoLCSC/
│
├── .github/
│   └── workflows/
│       ├── ci.yml                  # Continuous Integration
│       ├── release.yml             # GitHub Release automation
│       └── codeql-analysis.yml     # Security scanning
│
├── src/
│   └── lhatolcsc/
│       ├── __init__.py
│       ├── __main__.py             # Entry point
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   ├── client.py           # LCSC API client
│       │   ├── auth.py             # Authentication & signature
│       │   ├── endpoints.py        # API endpoints
│       │   └── models.py           # Data models (dataclasses)
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── bom_processor.py    # BOM file handling
│       │   ├── matcher.py          # Fuzzy matching logic
│       │   ├── config.py           # Configuration management
│       │   └── logger.py           # Logging setup
│       │
│       ├── gui/
│       │   ├── __init__.py
│       │   ├── main_window.py      # Main application window
│       │   ├── bom_panel.py        # BOM management panel
│       │   ├── search_panel.py     # Search & match panel
│       │   ├── results_panel.py    # Results display
│       │   ├── settings_dialog.py  # Settings/preferences
│       │   └── widgets/
│       │       ├── __init__.py
│       │       ├── fuzzy_search_box.py  # Custom fuzzy search widget
│       │       └── progress_bar.py      # Progress indicator
│       │
│       └── utils/
│           ├── __init__.py
│           ├── validators.py       # Input validation
│           ├── exporters.py        # Export functions
│           └── helpers.py          # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_client.py
│   │   └── test_auth.py
│   ├── test_core/
│   │   ├── __init__.py
│   │   ├── test_bom_processor.py
│   │   └── test_matcher.py
│   └── test_gui/
│       ├── __init__.py
│       └── test_main_window.py
│
├── docs/
│   ├── API_DOCUMENTATION.md        # LCSC API reference
│   ├── USER_GUIDE.md               # End-user documentation
│   ├── DEVELOPER_GUIDE.md          # Developer setup guide
│   └── CHANGELOG.md                # Version history
│
├── resources/
│   ├── icons/                      # Application icons
│   ├── config/
│   │   └── default_config.json     # Default configuration
│   └── templates/
│       └── sample_bom.xlsx         # Sample BOM template
│
├── scripts/
│   ├── build.py                    # Build script
│   └── release.py                  # Release preparation
│
├── .env.example                    # Example environment variables
├── .gitignore                      # Git ignore rules
├── .gitattributes                  # Git attributes
├── LICENSE                         # MIT License
├── README.md                       # Project README
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
├── setup.py                        # Package setup
├── pyproject.toml                  # Project metadata & tools
└── pytest.ini                      # Pytest configuration
```

---

## Core Features

### Phase 1: Foundation (Weeks 1-2)

#### 1.1 Project Setup
- [x] Research LCSC API documentation
- [ ] Initialize Git repository
- [ ] Set up Python virtual environment
- [ ] Configure development tools (Black, Flake8, MyPy)
- [ ] Create project structure
- [ ] Set up CI/CD pipeline (GitHub Actions)

#### 1.2 API Integration
- [ ] Implement authentication module (signature generation)
- [ ] Create LCSC API client base class
- [ ] Implement Keyword Search API endpoint
- [ ] Implement Product Details API endpoint
- [ ] Add error handling and retry logic
- [ ] Implement rate limiting
- [ ] Write unit tests for API module

#### 1.3 Configuration Management
- [ ] Create configuration file structure
- [ ] Implement settings manager
- [ ] Add API credentials management (secure storage)
- [ ] Add user preferences storage

### Phase 2: Core Functionality (Weeks 3-4)

#### 2.1 BOM Processing
- [ ] Implement Excel file reader (openpyxl/pandas)
- [ ] Add BOM structure validation
- [ ] Identify "Stock Part Name" column
- [ ] Create data models for BOM items
- [ ] Implement BOM export functionality
- [ ] Add support for multiple Excel formats

#### 2.2 Fuzzy Matching Engine
- [ ] Integrate fuzzy string matching library
- [ ] Implement matching algorithm
- [ ] Add confidence scoring
- [ ] Create match ranking system
- [ ] Add manual override options
- [ ] Implement caching for performance

### Phase 3: GUI Development (Weeks 5-6)

#### 3.1 Main Window
- [ ] Design main application layout
- [ ] Implement menu bar (File, Edit, Tools, Help)
- [ ] Add status bar with API status indicator
- [ ] Implement window state persistence

#### 3.2 BOM Management Panel
- [ ] File selection dialog
- [ ] BOM preview table (Treeview widget)
- [ ] Column mapping interface
- [ ] BOM validation indicators

#### 3.3 Search & Match Panel
- [ ] Custom fuzzy search box widget
- [ ] Real-time search as you type
- [ ] Search result preview
- [ ] Match confidence slider
- [ ] Batch processing controls

#### 3.4 Results Panel
- [ ] Matched results table
- [ ] Part details view
- [ ] Stock level indicators
- [ ] Pricing information display
- [ ] Manual selection interface

#### 3.5 Settings Dialog
- [ ] API credentials management
- [ ] Fuzzy match threshold configuration
- [ ] Export format preferences
- [ ] Theme selection (future)

### Phase 4: Advanced Features (Weeks 7-8)

#### 4.1 Enhanced Matching
- [ ] Multi-criteria matching (MPN, description, category)
- [ ] Learn from user selections (ML optional)
- [ ] Batch approval/rejection
- [ ] Alternative suggestions

#### 4.2 Export & Reporting
- [ ] Export enhanced BOM to Excel
- [ ] Add LCSC part numbers column
- [ ] Add pricing columns (unit, extended)
- [ ] Add stock availability column
- [ ] Generate matching report
- [ ] Export unmatched items list

#### 4.3 Performance Optimization
- [ ] Implement local caching (SQLite)
- [ ] Add multithreading for API calls
- [ ] Progress indicators for long operations
- [ ] Optimize large BOM handling (>1000 items)

### Phase 5: Testing & Documentation (Week 9)

#### 5.1 Testing
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests for API
- [ ] GUI tests (basic)
- [ ] End-to-end workflow tests
- [ ] Performance benchmarks

#### 5.2 Documentation
- [ ] API documentation
- [ ] User guide with screenshots
- [ ] Developer setup guide
- [ ] Code documentation (docstrings)
- [ ] README with quick start

### Phase 6: Release Management (Week 10)

#### 6.1 GitHub Release Setup
- [ ] Configure semantic versioning
- [ ] Set up automated changelog generation
- [ ] Create release workflow
- [ ] Add Windows executable build (PyInstaller)
- [ ] Create installer (optional)

#### 6.2 Deployment
- [ ] Tag v1.0.0 release
- [ ] Publish to GitHub Releases
- [ ] Create distribution package
- [ ] Write release notes

---

## User Workflow

### Typical User Journey

1. **Launch Application**
   - User starts LHAtoLCSC
   - Application loads configuration
   - API connection status checked

2. **Load BOM File**
   - User clicks "Load BOM" button
   - Selects Excel file from file dialog
   - Application parses and validates BOM
   - Preview displayed in table

3. **Configure Column Mapping**
   - Application auto-detects "Stock Part Name" column
   - User confirms or manually selects column
   - Additional columns mapped (Quantity, Reference, etc.)

4. **Initiate Fuzzy Search**
   - User clicks "Start Matching"
   - Application processes each BOM line:
     - Extracts part name from "Stock Part Name" column
     - Sends fuzzy search request to LCSC API
     - Receives multiple match candidates
     - Ranks by confidence score
   - Progress bar shows completion

5. **Review & Approve Matches**
   - Matched items displayed with confidence scores
   - Green indicator: High confidence (>90%)
   - Yellow indicator: Medium confidence (70-90%)
   - Red indicator: Low confidence (<70%)
   - User reviews and approves/modifies matches

6. **Export Enhanced BOM**
   - User clicks "Export BOM"
   - Application generates new Excel file with:
     - Original BOM columns
     - LCSC Part Number
     - LCSC Stock Level
     - Unit Price
     - Extended Price
     - Match Confidence
   - File saved to user-selected location

---

## Data Models

### BOMItem
```python
@dataclass
class BOMItem:
    row_index: int
    stock_part_name: str
    quantity: int
    reference_designator: str
    description: str = ""
    manufacturer: str = ""
    mpn: str = ""
    lcsc_part_number: str = ""
    match_confidence: float = 0.0
```

### LCSCProduct
```python
@dataclass
class LCSCProduct:
    product_number: str  # LCSC part number (e.g., C2653)
    product_code: str
    product_name: str
    manufacturer: str
    manufacturer_part: str  # MPN
    description: str
    category_id: int
    category_name: str
    stock: int
    price_tiers: List[PriceTier]
    datasheet_url: str
    image_url: str
    is_available: bool
    is_pre_sale: bool
```

### MatchResult
```python
@dataclass
class MatchResult:
    bom_item: BOMItem
    lcsc_product: Optional[LCSCProduct]
    match_score: float
    match_method: str  # "exact", "fuzzy", "manual"
    alternatives: List[LCSCProduct]
    matched_at: datetime
```

---

## API Integration Details

### Search Strategy

1. **Primary Search:** Fuzzy search on "Stock Part Name"
2. **Secondary Search:** If low confidence, search by MPN (if available)
3. **Tertiary Search:** Category + keyword combination

### Caching Strategy

- Cache search results locally (SQLite)
- TTL: 7 days for product information
- Cache key: SHA256(search_term + match_type)
- Reduces API calls and improves performance

### Error Handling

- Network errors: Retry with exponential backoff (3 attempts)
- Rate limit errors: Queue requests and resume
- Authentication errors: Prompt user to re-enter credentials
- Invalid responses: Log and skip item with error flag

---

## Git Workflow & Release Management

### Branch Strategy

- **main:** Production-ready code
- **develop:** Integration branch for features
- **feature/*:** Individual feature development
- **bugfix/*:** Bug fixes
- **release/*:** Release preparation

### Commit Convention

Follow Conventional Commits:
```
feat: Add fuzzy search box widget
fix: Correct API signature generation
docs: Update user guide with screenshots
test: Add unit tests for BOM processor
refactor: Simplify matcher logic
chore: Update dependencies
```

### GitHub Actions Workflows

#### CI Pipeline (.github/workflows/ci.yml)
```yaml
- Trigger: Push to any branch, PRs
- Jobs:
  - Lint (Black, Flake8, MyPy)
  - Test (pytest with coverage)
  - Build (verify package builds)
```

#### Release Pipeline (.github/workflows/release.yml)
```yaml
- Trigger: Tag push (v*.*.*)
- Jobs:
  - Build package
  - Create GitHub Release
  - Upload artifacts (wheel, exe)
  - Generate changelog
```

### Release Process

1. Update version in `setup.py` and `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release branch: `release/v1.0.0`
4. Test release candidate
5. Merge to `main`
6. Tag release: `git tag -a v1.0.0 -m "Release v1.0.0"`
7. Push tag: `git push origin v1.0.0`
8. GitHub Actions automatically creates release

### Versioning (Semantic Versioning)

- **MAJOR:** Breaking changes (e.g., 2.0.0)
- **MINOR:** New features, backward compatible (e.g., 1.1.0)
- **PATCH:** Bug fixes (e.g., 1.0.1)

---

## Security Considerations

1. **API Credentials:**
   - Store in `.env` file (never commit)
   - Use `python-dotenv` for loading
   - Encrypt credentials in config file (optional)

2. **Input Validation:**
   - Sanitize all user inputs
   - Validate Excel file structure
   - Prevent path traversal attacks

3. **Network Security:**
   - Use HTTPS for all API calls
   - Verify SSL certificates
   - Implement request timeout

4. **Data Privacy:**
   - Don't log sensitive data
   - Clear cache option
   - GDPR compliance (if applicable)

---

## Performance Targets

- **BOM Loading:** < 2 seconds for 1,000 line BOM
- **Single Part Search:** < 1 second (including network)
- **Batch Processing:** 50-100 parts/minute (API rate limit dependent)
- **Large BOM (5,000 lines):** < 60 minutes with caching
- **Memory Usage:** < 200 MB for typical operations
- **Application Startup:** < 3 seconds

---

## Future Enhancements (Post v1.0)

### Phase 2 Features
- [ ] Direct ordering from application (Order API)
- [ ] Price comparison across multiple distributors
- [ ] Inventory management integration
- [ ] Multi-language support
- [ ] Dark theme option

### Phase 3 Features
- [ ] Web-based version (Flask/FastAPI)
- [ ] Mobile companion app
- [ ] Cloud sync for BOM storage
- [ ] Collaborative features (team BOM sharing)
- [ ] ML-based matching improvements

---

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| API changes breaking compatibility | High | Medium | Version API client, monitor LCSC announcements |
| Rate limiting affecting UX | Medium | High | Implement caching, batch optimization |
| Excel format variations | Medium | Medium | Support multiple formats, validation |
| Fuzzy matching false positives | Medium | High | Manual review step, confidence thresholds |
| API key security leak | High | Low | .env file, .gitignore, user education |

---

## Success Metrics

- **Accuracy:** >95% correct matches for common components
- **Speed:** Process 100-part BOM in < 5 minutes
- **User Satisfaction:** Reduce manual part lookup time by 80%
- **Reliability:** 99% uptime (dependent on LCSC API)
- **Adoption:** 100+ GitHub stars within 6 months

---

## Team & Resources

### Required Skills
- Python development (intermediate to advanced)
- Tkinter GUI development
- REST API integration
- Excel file processing
- Git/GitHub workflow

### Development Environment
- **OS:** Windows 10/11 (primary), macOS/Linux (testing)
- **Python:** 3.10+
- **IDE:** VS Code with Python extension
- **Version Control:** Git + GitHub
- **Package Manager:** pip + virtual environment

---

## Maintenance Plan

### Post-Launch Support
- **Bug Fixes:** Within 48 hours for critical issues
- **Feature Requests:** Quarterly release cycle
- **API Updates:** Monitor and adapt within 1 week
- **Security Patches:** Immediate for critical vulnerabilities

### Documentation Updates
- Update with each minor/major release
- Maintain changelog
- User guide updates for new features

---

## Appendices

### Appendix A: LCSC API Endpoints Quick Reference

```
Base URL: https://www.lcsc.com

1. Keyword Search (Primary):
   GET /rest/wmsc2agent/search/product
   
2. Product Details:
   GET /rest/wmsc2agent/product/info/{product_number}
   
3. Category List:
   GET /rest/wmsc2agent/category
   
4. Brand List:
   GET /rest/wmsc2agent/brand
```

### Appendix B: Sample API Request

```python
import hashlib
import time
import requests

def create_signature(key, secret, timestamp, nonce):
    params = f"key={key}&nonce={nonce}&secret={secret}&timestamp={timestamp}"
    return hashlib.sha1(params.encode()).hexdigest()

# Example search request
key = "your_api_key"
secret = "your_api_secret"
timestamp = str(int(time.time()))
nonce = "a1b2c3d4e5f6g7h8"

signature = create_signature(key, secret, timestamp, nonce)

params = {
    "key": key,
    "timestamp": timestamp,
    "nonce": nonce,
    "signature": signature,
    "keyword": "STM32F103",
    "match_type": "fuzzy",
    "page_size": 30
}

response = requests.get(
    "https://www.lcsc.com/rest/wmsc2agent/search/product",
    params=params
)
```

### Appendix C: Sample BOM Structure

| Stock Part Name | Quantity | Reference Designator | Description |
|----------------|----------|----------------------|-------------|
| STM32F103C8T6 | 1 | U1 | Microcontroller |
| 10K Resistor 0603 | 10 | R1-R10 | Resistor |
| 100nF Capacitor 0603 | 15 | C1-C15 | Ceramic Capacitor |

---

## Conclusion

LHAtoLCSC will significantly streamline the component sourcing process by automating the tedious task of matching BOM items with LCSC part numbers. With a professional architecture, comprehensive testing, and proper release management, this tool will provide reliable and efficient service to electronics engineers and procurement specialists.

**Project Timeline:** 10 weeks to v1.0.0 release  
**Estimated Effort:** 200-250 development hours  
**Target Launch:** Q1 2026

---

**Document Version:** 1.0  
**Last Updated:** October 21, 2025  
**Author:** Development Team  
**Status:** Draft - Ready for Implementation
