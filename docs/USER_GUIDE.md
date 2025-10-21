# LHAtoLCSC User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Using the Application](#using-the-application)
5. [BOM File Format](#bom-file-format)
6. [Troubleshooting](#troubleshooting)

## Introduction

LHAtoLCSC is a desktop application that helps you match components from your Bill of Materials (BOM) with LCSC electronic parts automatically using intelligent fuzzy search.

## Installation

### Prerequisites

- Python 3.10 or higher
- LCSC API credentials ([Apply here](https://www.lcsc.com/agent))

### Installation Steps

1. Download the latest release from GitHub
2. Extract to your desired location
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure API credentials (see Configuration section)

## Getting Started

### Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your LCSC API credentials:
   ```
   LCSC_API_KEY=your_api_key_here
   LCSC_API_SECRET=your_api_secret_here
   ```

### First Launch

1. Run the application:
   ```bash
   python -m src.lhatolcsc
   ```

2. Test your API connection:
   - Click **Tools → Test API Connection**
   - You should see a success message

## Using the Application

### Step 1: Prepare Your BOM

Ensure your Excel file has:
- A column for part names (e.g., "Stock Part Name")
- A column for quantities
- A column for reference designators (optional)

### Step 2: Load BOM File

1. Click **File → Load BOM...**
2. Select your Excel file (.xlsx, .xls, or .csv)
3. The application will auto-detect columns
4. Verify the column mapping

### Step 3: Start Matching

1. Click **Start Matching**
2. Wait for the fuzzy search to complete
3. Review match confidence scores:
   - 🟢 Green (>90%): High confidence
   - 🟡 Yellow (70-90%): Medium confidence
   - 🔴 Red (<70%): Low confidence - requires review

### Step 4: Review and Approve

1. Review each match
2. Click on items to see alternatives
3. Manually select correct part if needed
4. Add notes for problematic matches

### Step 5: Export Enhanced BOM

1. Click **File → Export BOM...**
2. Choose save location
3. Your BOM now includes:
   - LCSC Part Numbers
   - Stock levels
   - Pricing information
   - Match confidence scores

## BOM File Format

### Required Columns

- **Stock Part Name**: Component description or part number

### Optional Columns

- **Quantity**: Number of components needed
- **Reference Designator**: PCB reference (e.g., R1, C5, U3)
- **Description**: Additional part details
- **Manufacturer**: Component manufacturer
- **MPN**: Manufacturer Part Number

### Sample BOM

| Stock Part Name | Quantity | Reference Designator | Description |
|----------------|----------|----------------------|-------------|
| STM32F103C8T6 | 1 | U1 | ARM Microcontroller |
| 10K Resistor 0603 | 10 | R1-R10 | 1% 0.1W |
| 100nF Capacitor | 15 | C1-C15 | X7R 50V |

## Troubleshooting

### API Connection Fails

**Problem**: "API connection failed" message

**Solutions**:
1. Verify your API credentials in `.env`
2. Check internet connection
3. Ensure API key is active (not expired)
4. Check LCSC API status

### No Matches Found

**Problem**: Search returns no matches for known parts

**Solutions**:
1. Check part name spelling
2. Try removing packaging info (e.g., "-TR", "REEL")
3. Use manufacturer part number instead
4. Search LCSC website manually to verify part exists

### Low Match Confidence

**Problem**: Matches have low confidence scores

**Solutions**:
1. Refine part names in BOM
2. Include manufacturer part numbers
3. Adjust fuzzy match threshold in settings
4. Manually select correct alternative

### Excel File Won't Load

**Problem**: Error loading BOM file

**Solutions**:
1. Ensure file is valid Excel format (.xlsx, .xls, .csv)
2. Check file isn't password protected
3. Verify file isn't corrupted
4. Close file in other applications

### Rate Limit Errors

**Problem**: "Rate limit exceeded" message

**Solutions**:
1. Wait 1 minute before retrying
2. Process smaller batches
3. Request higher rate limits from LCSC
4. Enable caching in settings

## Tips for Best Results

1. **Standardize Part Names**: Use consistent naming in your BOM
2. **Include MPNs**: Add manufacturer part numbers for better matching
3. **Review Matches**: Always verify high-value or critical components
4. **Save Progress**: Export intermediate results frequently
5. **Use Cache**: Enable caching for faster repeated searches

## Getting Help

- **Email**: support@example.com
- **GitHub Issues**: [Report a bug](https://github.com/yourusername/LHAtoLCSC/issues)
- **Documentation**: See additional docs in `/docs` folder

---

**Version**: 0.1.0  
**Last Updated**: October 21, 2025
