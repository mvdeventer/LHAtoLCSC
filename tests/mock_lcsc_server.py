"""
Mock LCSC API Server for Testing

This is a simple Flask server that simulates the LCSC API for testing purposes.
Run this server locally and point your application to http://localhost:5000

Usage:
    python tests/mock_lcsc_server.py

Mock Credentials:
    API Key: test_api_key_12345
    API Secret: test_api_secret_67890
"""

from flask import Flask, request, jsonify
import hashlib
import time
import json
import os
from typing import Dict, Any

app = Flask(__name__)

# Mock credentials
VALID_API_KEY = "test_api_key_12345"
VALID_API_SECRET = "test_api_secret_67890"

# Load large product database
print("Loading product database...")
LARGE_DB_PATH = os.path.join(os.path.dirname(__file__), 'mock_products_large.json')
if os.path.exists(LARGE_DB_PATH):
    with open(LARGE_DB_PATH, 'r') as f:
        MOCK_PRODUCTS_LARGE = json.load(f)
    print(f"Loaded {len(MOCK_PRODUCTS_LARGE)} products from {LARGE_DB_PATH}")
else:
    print(f"Large database not found at {LARGE_DB_PATH}, using small database")
    MOCK_PRODUCTS_LARGE = {}

# Mock product database - Comprehensive LCSC components (small set for quick testing)
MOCK_PRODUCTS = {
    # Resistors - Surface Mount
    "C17572": {
        "productCode": "C17572",
        "productModel": "0603WAF1002T5E",
        "productName": "RES 10K OHM 1% 1/10W 0603",
        "brandName": "UNI-ROYAL(Uniroyal Elec)",
        "packageType": "0603",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "125000",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0005", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0004", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0003", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Resistance", "paramValue": "10KΩ"},
            {"paramCode": "Tolerance", "paramValue": "±1%"},
            {"paramCode": "Power", "paramValue": "1/10W"}
        ]
    },
    "C25804": {
        "productCode": "C25804",
        "productModel": "0603WAF1001T5E",
        "productName": "RES 1K OHM 1% 1/10W 0603",
        "brandName": "UNI-ROYAL(Uniroyal Elec)",
        "packageType": "0603",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "98700",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0005", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0004", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0003", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Resistance", "paramValue": "1KΩ"},
            {"paramCode": "Tolerance", "paramValue": "±1%"},
            {"paramCode": "Power", "paramValue": "1/10W"}
        ]
    },
    "C22790": {
        "productCode": "C22790",
        "productModel": "0603WAF4701T5E",
        "productName": "RES 4.7K OHM 1% 1/10W 0603",
        "brandName": "UNI-ROYAL(Uniroyal Elec)",
        "packageType": "0603",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "156000",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0005", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0004", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0003", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Resistance", "paramValue": "4.7KΩ"},
            {"paramCode": "Tolerance", "paramValue": "±1%"},
            {"paramCode": "Power", "paramValue": "1/10W"}
        ]
    },
    
    # Capacitors - Ceramic
    "C15849": {
        "productCode": "C15849",
        "productModel": "CL10A475KO8NNNC",
        "productName": "CAP CER 4.7UF 16V X5R 0603",
        "brandName": "SAMSUNG",
        "packageType": "0603",
        "productUnit": "pcs",
        "minPacketUnit": "4000",
        "minBuyNumber": "1",
        "stockNumber": "89500",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0234", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0189", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0154", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Capacitance", "paramValue": "4.7µF"},
            {"paramCode": "Voltage", "paramValue": "16V"},
            {"paramCode": "Tolerance", "paramValue": "±10%"}
        ]
    },
    "C14663": {
        "productCode": "C14663",
        "productModel": "CL10B104KB8NNNC",
        "productName": "CAP CER 100NF 50V X7R 0603",
        "brandName": "SAMSUNG",
        "packageType": "0603",
        "productUnit": "pcs",
        "minPacketUnit": "4000",
        "minBuyNumber": "1",
        "stockNumber": "245000",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0078", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0062", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0051", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Capacitance", "paramValue": "100nF"},
            {"paramCode": "Voltage", "paramValue": "50V"},
            {"paramCode": "Tolerance", "paramValue": "±10%"}
        ]
    },
    "C1525": {
        "productCode": "C1525",
        "productModel": "CL10C220JB8NNNC",
        "productName": "CAP CER 22PF 50V C0G/NP0 0603",
        "brandName": "SAMSUNG",
        "packageType": "0603",
        "productUnit": "pcs",
        "minPacketUnit": "4000",
        "minBuyNumber": "1",
        "stockNumber": "67800",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0045", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0036", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0029", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Capacitance", "paramValue": "22pF"},
            {"paramCode": "Voltage", "paramValue": "50V"},
            {"paramCode": "Tolerance", "paramValue": "±5%"}
        ]
    },
    
    # Capacitors - Electrolytic
    "C134502": {
        "productCode": "C134502",
        "productModel": "CA035M0100REF-0605",
        "productName": "CAP ALUM 100UF 35V 20% RADIAL",
        "brandName": "LELON",
        "packageType": "Plugin,D6.3xL5mm",
        "productUnit": "pcs",
        "minPacketUnit": "1000",
        "minBuyNumber": "1",
        "stockNumber": "12500",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0456", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0367", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0298", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Capacitance", "paramValue": "100µF"},
            {"paramCode": "Voltage", "paramValue": "35V"},
            {"paramCode": "Tolerance", "paramValue": "±20%"},
            {"paramCode": "ESR", "paramValue": "1.5Ω@100kHz"}
        ]
    },
    
    # Microcontrollers
    "C2040": {
        "productCode": "C2040",
        "productModel": "STM32F103C8T6",
        "productName": "MCU ARM 32BIT 64KB FLASH LQFP48",
        "brandName": "STMicroelectronics",
        "packageType": "LQFP-48",
        "productUnit": "pcs",
        "minPacketUnit": "1",
        "minBuyNumber": "1",
        "stockNumber": "5420",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "2.8500", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "2.3000", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "1.9800", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Core", "paramValue": "ARM Cortex-M3"},
            {"paramCode": "Flash", "paramValue": "64KB"},
            {"paramCode": "RAM", "paramValue": "20KB"}
        ]
    },
    "C20038": {
        "productCode": "C20038",
        "productModel": "STM32F103RCT6",
        "productName": "MCU ARM 32BIT 256KB FLASH LQFP64",
        "brandName": "STMicroelectronics",
        "packageType": "LQFP-64",
        "productUnit": "pcs",
        "minPacketUnit": "1",
        "minBuyNumber": "1",
        "stockNumber": "3200",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "4.5600", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "4.1200", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "3.2400", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Core", "paramValue": "ARM Cortex-M3"},
            {"paramCode": "Flash Size", "paramValue": "256KB"},
            {"paramCode": "RAM Size", "paramValue": "48KB"},
            {"paramCode": "Speed", "paramValue": "72MHz"}
        ]
    },
    "C82507": {
        "productCode": "C82507",
        "productModel": "ESP32-WROOM-32",
        "productName": "WiFi Modules SMD Module,27x18x3.1mm",
        "brandName": "Espressif Systems",
        "packageType": "SMD-38",
        "productUnit": "pcs",
        "minPacketUnit": "1",
        "minBuyNumber": "1",
        "stockNumber": "8900",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "2.1500", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "1.9800", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "1.6500", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Core", "paramValue": "ESP32-D0WDQ6"},
            {"paramCode": "Flash Size", "paramValue": "4MB"},
            {"paramCode": "WiFi", "paramValue": "802.11 b/g/n"},
            {"paramCode": "Bluetooth", "paramValue": "v4.2 BR/EDR and BLE"}
        ]
    },
    
    # LEDs
    "C72041": {
        "productCode": "C72041",
        "productModel": "17-21/BHC-ZL1M2RY/3T",
        "productName": "LED RED CLEAR 0603 SMD",
        "brandName": "Everlight Elec",
        "packageType": "0603",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "45600",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0234", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0189", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0145", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Color", "paramValue": "Red"},
            {"paramCode": "Wavelength", "paramValue": "625nm"},
            {"paramCode": "Forward Voltage", "paramValue": "2.0V"},
            {"paramCode": "Luminous Intensity", "paramValue": "35mcd"}
        ]
    },
    "C72043": {
        "productCode": "C72043",
        "productModel": "17-21/G6C-AL1M2VY/3T",
        "productName": "LED GREEN CLEAR 0603 SMD",
        "brandName": "Everlight Elec",
        "packageType": "0603",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "38900",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0234", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0189", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0145", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Color", "paramValue": "Green"},
            {"paramCode": "Wavelength", "paramValue": "525nm"},
            {"paramCode": "Forward Voltage", "paramValue": "3.0V"},
            {"paramCode": "Luminous Intensity", "paramValue": "45mcd"}
        ]
    },
    
    # Diodes
    "C81598": {
        "productCode": "C81598",
        "productModel": "1N4148W",
        "productName": "DIODE SWITCH 75V 150MA SOD-123",
        "brandName": "Changjiang Electronics Tech (CJ)",
        "packageType": "SOD-123",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "234000",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0089", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0071", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0058", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Type", "paramValue": "Switching"},
            {"paramCode": "Voltage", "paramValue": "75V"},
            {"paramCode": "Current", "paramValue": "150mA"},
            {"paramCode": "Recovery Time", "paramValue": "4ns"}
        ]
    },
    "C8678": {
        "productCode": "C8678",
        "productModel": "SS34",
        "productName": "DIODE SCHOTTKY 40V 3A SMA",
        "brandName": "MDD(Microdiode Electronics)",
        "packageType": "SMA(DO-214AC)",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "145000",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0345", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0278", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0226", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Type", "paramValue": "Schottky"},
            {"paramCode": "Voltage", "paramValue": "40V"},
            {"paramCode": "Current", "paramValue": "3A"},
            {"paramCode": "Forward Voltage", "paramValue": "0.5V@3A"}
        ]
    },
    
    # Transistors - MOSFETs
    "C20917": {
        "productCode": "C20917",
        "productModel": "AO3401A",
        "productName": "MOSFET P-CH 30V 4A SOT-23",
        "brandName": "ALPHA & OMEGA Semicon",
        "packageType": "SOT-23",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "89000",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0456", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0367", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0298", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Type", "paramValue": "P-Channel"},
            {"paramCode": "Voltage", "paramValue": "30V"},
            {"paramCode": "Current", "paramValue": "4A"},
            {"paramCode": "RDS(on)", "paramValue": "44mΩ@10V"}
        ]
    },
    "C20941": {
        "productCode": "C20941",
        "productModel": "AO3400A",
        "productName": "MOSFET N-CH 30V 5.7A SOT-23",
        "brandName": "ALPHA & OMEGA Semicon",
        "packageType": "SOT-23",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "125000",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0389", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0314", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0255", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Type", "paramValue": "N-Channel"},
            {"paramCode": "Voltage", "paramValue": "30V"},
            {"paramCode": "Current", "paramValue": "5.7A"},
            {"paramCode": "RDS(on)", "paramValue": "27mΩ@10V"}
        ]
    },
    
    # Voltage Regulators
    "C5446": {
        "productCode": "C5446",
        "productModel": "AMS1117-3.3",
        "productName": "LDO REGULATOR 3.3V 1A SOT-223",
        "brandName": "Advanced Monolithic Systems",
        "packageType": "SOT-223",
        "productUnit": "pcs",
        "minPacketUnit": "1000",
        "minBuyNumber": "1",
        "stockNumber": "45600",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0567", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0456", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0371", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Type", "paramValue": "LDO"},
            {"paramCode": "Output Voltage", "paramValue": "3.3V"},
            {"paramCode": "Current", "paramValue": "1A"},
            {"paramCode": "Dropout Voltage", "paramValue": "1.3V@1A"}
        ]
    },
    "C6186": {
        "productCode": "C6186",
        "productModel": "AMS1117-5.0",
        "productName": "LDO REGULATOR 5.0V 1A SOT-223",
        "brandName": "Advanced Monolithic Systems",
        "packageType": "SOT-223",
        "productUnit": "pcs",
        "minPacketUnit": "1000",
        "minBuyNumber": "1",
        "stockNumber": "32100",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0567", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0456", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0371", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Type", "paramValue": "LDO"},
            {"paramCode": "Output Voltage", "paramValue": "5.0V"},
            {"paramCode": "Current", "paramValue": "1A"},
            {"paramCode": "Dropout Voltage", "paramValue": "1.3V@1A"}
        ]
    },
    
    # Crystals & Oscillators
    "C9002": {
        "productCode": "C9002",
        "productModel": "X322516MLB4SI",
        "productName": "CRYSTAL 16.000MHZ 20PF SMD",
        "brandName": "Yangxing Tech",
        "packageType": "HC-49S-SMD",
        "productUnit": "pcs",
        "minPacketUnit": "1000",
        "minBuyNumber": "1",
        "stockNumber": "67800",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0678", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0545", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0443", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Frequency", "paramValue": "16MHz"},
            {"paramCode": "Load Capacitance", "paramValue": "20pF"},
            {"paramCode": "Tolerance", "paramValue": "±20ppm"},
            {"paramCode": "Operating Temperature", "paramValue": "-20°C ~ 70°C"}
        ]
    },
    "C12674": {
        "productCode": "C12674",
        "productModel": "X322532768MSB4SI",
        "productName": "CRYSTAL 32.768KHZ 12.5PF SMD",
        "brandName": "Yangxing Tech",
        "packageType": "2P-3.2x1.5mm",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "89400",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0789", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0634", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0515", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Frequency", "paramValue": "32.768kHz"},
            {"paramCode": "Load Capacitance", "paramValue": "12.5pF"},
            {"paramCode": "Tolerance", "paramValue": "±20ppm"},
            {"paramCode": "Operating Temperature", "paramValue": "-40°C ~ 85°C"}
        ]
    },
    
    # Connectors
    "C16214": {
        "productCode": "C16214",
        "productModel": "USB-A-S-RA",
        "productName": "USB TYPE-A RECEPTACLE R/A SMT",
        "brandName": "SHOU HAN",
        "packageType": "SMD",
        "productUnit": "pcs",
        "minPacketUnit": "100",
        "minBuyNumber": "1",
        "stockNumber": "12300",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.1234", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0989", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0804", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Type", "paramValue": "USB Type-A"},
            {"paramCode": "Gender", "paramValue": "Receptacle"},
            {"paramCode": "Mounting", "paramValue": "Surface Mount"},
            {"paramCode": "Orientation", "paramValue": "Right Angle"}
        ]
    },
    "C167321": {
        "productCode": "C167321",
        "productModel": "TYPE-C-31-M-12",
        "productName": "USB TYPE-C RECEPTACLE SMT 16P",
        "brandName": "Korean Hroparts Elec",
        "packageType": "SMD",
        "productUnit": "pcs",
        "minPacketUnit": "50",
        "minBuyNumber": "1",
        "stockNumber": "8900",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.2345", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.1889", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.1535", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Type", "paramValue": "USB Type-C"},
            {"paramCode": "Gender", "paramValue": "Receptacle"},
            {"paramCode": "Pins", "paramValue": "16"},
            {"paramCode": "Mounting", "paramValue": "Surface Mount"}
        ]
    },
    
    # Op-Amps
    "C7950": {
        "productCode": "C7950",
        "productModel": "LM358",
        "productName": "OP AMP DUAL GP 700KHZ 8SOIC",
        "brandName": "Texas Instruments",
        "packageType": "SOIC-8",
        "productUnit": "pcs",
        "minPacketUnit": "50",
        "minBuyNumber": "1",
        "stockNumber": "23400",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.1567", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.1256", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.1022", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Number of Channels", "paramValue": "2"},
            {"paramCode": "Bandwidth", "paramValue": "700kHz"},
            {"paramCode": "Supply Voltage", "paramValue": "3V ~ 32V"},
            {"paramCode": "Slew Rate", "paramValue": "0.3V/µs"}
        ]
    },
    
    # Inductors
    "C1017": {
        "productCode": "C1017",
        "productModel": "SDFL2012S100KTF",
        "productName": "INDUCTOR 10UH 20% 300MA 0805",
        "brandName": "Sunlord",
        "packageType": "0805",
        "productUnit": "pcs",
        "minPacketUnit": "3000",
        "minBuyNumber": "1",
        "stockNumber": "45600",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0234", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0189", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0154", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Inductance", "paramValue": "10µH"},
            {"paramCode": "Tolerance", "paramValue": "±20%"},
            {"paramCode": "Current", "paramValue": "300mA"},
            {"paramCode": "DCR", "paramValue": "0.8Ω"}
        ]
    },
    
    # Buttons & Switches
    "C318884": {
        "productCode": "C318884",
        "productModel": "TS-1187A-B-A-B",
        "productName": "TACTILE SWITCH SMD 5.2x5.2mm",
        "brandName": "XKB Connectivity",
        "packageType": "SMD,5.2x5.2mm",
        "productUnit": "pcs",
        "minPacketUnit": "1000",
        "minBuyNumber": "1",
        "stockNumber": "67800",
        "productPriceList": [
            {"startNumber": "1", "productPrice": "0.0345", "discountRate": "100"},
            {"startNumber": "10", "productPrice": "0.0278", "discountRate": "100"},
            {"startNumber": "100", "productPrice": "0.0226", "discountRate": "100"}
        ],
        "paramVOList": [
            {"paramCode": "Type", "paramValue": "Tactile"},
            {"paramCode": "Actuator Height", "paramValue": "1.5mm"},
            {"paramCode": "Operating Force", "paramValue": "160gf"},
            {"paramCode": "Life Cycle", "paramValue": "100,000 cycles"}
        ]
    }
}


def verify_signature(api_key: str, api_secret: str, timestamp: str, nonce: str, signature: str) -> bool:
    """Verify the API signature (simplified version)."""
    # In real LCSC API, this would be more complex
    # For mock, just check if key and secret match
    return api_key == VALID_API_KEY and api_secret == VALID_API_SECRET


def check_auth() -> Dict[str, Any]:
    """Check authentication from query parameters (LCSC API style)."""
    # LCSC API uses query parameters: key, timestamp, nonce, signature
    api_key = request.args.get('key', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    signature = request.args.get('signature', '')
    
    # Fallback to headers for backward compatibility
    if not api_key:
        api_key = request.headers.get('X-API-KEY', '')
    
    if not api_key:
        return {
            "success": False,
            "code": 401,
            "message": "Missing API key",
            "result": None
        }
    
    if api_key != VALID_API_KEY:
        return {
            "success": False,
            "code": 401,
            "message": "Invalid API key",
            "result": None
        }
    
    # For mock server, we accept any signature as long as key is valid
    # In production, you'd verify: SHA1(key + secret + timestamp + nonce)
    if not signature:
        return {
            "success": False,
            "code": 401,
            "message": "Missing signature",
            "result": None
        }
    
    return {"success": True}


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "Mock LCSC API Server is running",
        "version": "1.0.0"
    })


@app.route('/rest/wmsc2agent/search/product', methods=['POST', 'GET'])
def search_products():
    """Search products endpoint - matches real LCSC API."""
    auth = check_auth()
    if not auth.get("success"):
        return jsonify(auth), 401
    
    # Get search parameters (LCSC uses different param names)
    if request.method == 'POST':
        data = request.get_json() or {}
    else:
        data = request.args.to_dict()
    
    keyword = data.get('keyword', '').lower()
    current_page = int(data.get('current_page', 1))
    page_size = int(data.get('page_size', 10))
    
    # Use large database if available, otherwise use small database
    db = MOCK_PRODUCTS_LARGE if MOCK_PRODUCTS_LARGE else MOCK_PRODUCTS
    
    # Filter products based on keyword
    results = []
    for code, product in db.items():
        if (keyword in product['productModel'].lower() or
            keyword in product['productName'].lower() or
            keyword in code.lower()):
            results.append(product)
    
    # Paginate
    start = (current_page - 1) * page_size
    end = start + page_size
    paginated = results[start:end]
    
    return jsonify({
        "success": True,
        "code": 200,
        "message": "Success",
        "result": {
            "total": len(results),
            "current_page": current_page,
            "page_size": page_size,
            "list": paginated
        }
    })


@app.route('/rest/wmsc2agent/product/info/<product_code>', methods=['GET'])
def get_product_detail(product_code: str):
    """Get product detail by product code - matches real LCSC API."""
    auth = check_auth()
    if not auth.get("success"):
        return jsonify(auth), 401
    
    # Use large database if available, otherwise use small database
    db = MOCK_PRODUCTS_LARGE if MOCK_PRODUCTS_LARGE else MOCK_PRODUCTS
    product = db.get(product_code)
    
    if not product:
        return jsonify({
            "success": False,
            "code": 404,
            "message": f"Product {product_code} not found",
            "result": None
        }), 404
    
    return jsonify({
        "success": True,
        "code": 200,
        "message": "Success",
        "result": product
    })


@app.route('/rest/wmsc2agent/category', methods=['GET'])
def get_category_tree():
    """Get category tree - matches real LCSC API."""
    auth = check_auth()
    if not auth.get("success"):
        return jsonify(auth), 401
    
    categories = [
        {
            "categoryId": "1",
            "categoryName": "Resistors",
            "parentId": "0",
            "children": [
                {"categoryId": "101", "categoryName": "Chip Resistor - Surface Mount", "parentId": "1", "children": []},
                {"categoryId": "102", "categoryName": "Through Hole Resistors", "parentId": "1", "children": []}
            ]
        },
        {
            "categoryId": "2",
            "categoryName": "Capacitors",
            "parentId": "0",
            "children": [
                {"categoryId": "201", "categoryName": "Multilayer Ceramic Capacitors MLCC - SMD/SMT", "parentId": "2", "children": []},
                {"categoryId": "202", "categoryName": "Aluminum Electrolytic Capacitors", "parentId": "2", "children": []}
            ]
        },
        {
            "categoryId": "3",
            "categoryName": "Integrated Circuits (ICs)",
            "parentId": "0",
            "children": [
                {"categoryId": "301", "categoryName": "Microcontrollers - MCU", "parentId": "3", "children": []},
                {"categoryId": "302", "categoryName": "Interface ICs", "parentId": "3", "children": []}
            ]
        }
    ]
    
    return jsonify({
        "success": True,
        "code": 200,
        "message": "Success",
        "result": categories
    })


@app.route('/rest/wmsc2agent/brand', methods=['GET'])
def get_brands():
    """Get brand list - matches real LCSC API."""
    auth = check_auth()
    if not auth.get("success"):
        return jsonify(auth), 401
    
    brands = [
        {"brandId": "1", "brandName": "UNI-ROYAL(Uniroyal Elec)"},
        {"brandId": "2", "brandName": "SAMSUNG"},
        {"brandId": "3", "brandName": "STMicroelectronics"},
        {"brandId": "4", "brandName": "Texas Instruments"},
        {"brandId": "5", "brandName": "NXP"},
    ]
    
    return jsonify({
        "success": True,
        "code": 200,
        "message": "Success",
        "result": brands
    })


# Keep old endpoints for backward compatibility
@app.route('/api/products/search', methods=['POST', 'GET'])
def search_products_old():
    """Legacy endpoint - redirect to new one."""
    return search_products()


@app.route('/api/products/detail/<product_code>', methods=['GET'])
def get_product_detail_old(product_code: str):
    """Legacy endpoint - redirect to new one."""
    return get_product_detail(product_code)


@app.route('/rest/wmsc2agent/product/batch', methods=['POST'])
def batch_products():
    """Get multiple products by product codes - matches real LCSC API."""
    auth = check_auth()
    if not auth.get("success"):
        return jsonify(auth), 401
    
    data = request.get_json() or {}
    product_codes = data.get('productCodes', [])
    
    # Use large database if available, otherwise use small database
    db = MOCK_PRODUCTS_LARGE if MOCK_PRODUCTS_LARGE else MOCK_PRODUCTS
    
    results = []
    for code in product_codes:
        if code in db:
            results.append(db[code])
    
    return jsonify({
        "success": True,
        "code": 200,
        "message": "Success",
        "result": results
    })


@app.route('/api/test/connection', methods=['GET', 'POST'])
def test_connection():
    """Test API connection endpoint."""
    auth = check_auth()
    if not auth.get("success"):
        return jsonify(auth), 401
    
    return jsonify({
        "success": True,
        "code": 200,
        "message": "Connection successful! Your credentials are valid.",
        "result": {
            "timestamp": int(time.time()),
            "apiKey": request.headers.get('X-API-KEY', request.args.get('apiKey')),
            "serverTime": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "code": 404,
        "message": "Endpoint not found",
        "result": None
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({
        "success": False,
        "code": 500,
        "message": "Internal server error",
        "result": None
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Mock LCSC API Server")
    print("=" * 60)
    print()
    print("Server URL: http://localhost:5000")
    print()
    print("Mock Credentials:")
    print(f"  API Key:    {VALID_API_KEY}")
    print(f"  API Secret: {VALID_API_SECRET}")
    print()
    print("Available Endpoints:")
    print("  GET  /health                      - Health check")
    print("  POST /rest/wmsc2agent/search/product      - Search products")
    print("  GET  /rest/wmsc2agent/product/info/<code> - Get product details")
    print("  POST /rest/wmsc2agent/product/batch       - Batch get products")
    print("  GET  /rest/wmsc2agent/category            - Get categories")
    print("  GET  /rest/wmsc2agent/brand               - Get brands")
    print("  GET  /api/test/connection                 - Test connection")
    print()
    
    # Show database stats
    if MOCK_PRODUCTS_LARGE:
        print(f"🗄️  Product Database: {len(MOCK_PRODUCTS_LARGE):,} components (LARGE DATABASE)")
        print(f"   Product codes: C100000 to C{100000 + len(MOCK_PRODUCTS_LARGE) - 1}")
        print(f"   Categories: Resistors, Capacitors, Inductors, Crystals")
        print(f"   Manufacturers: 10+ brands with multiple packages")
    else:
        print(f"Mock Products Available ({len(MOCK_PRODUCTS)} components):")
    
    print()
    print("Small Database Also Available (25 quick-test components):")
    print("  Resistors: C17572, C25804, C22790")
    print("  Capacitors: C15849, C14663, C1525, C134502")
    print("  MCUs: C2040, C20038, C82507")
    print("  LEDs: C72041, C72043")
    print("  Diodes: C81598, C8678")
    print("  MOSFETs: C20917, C20941")
    print("  Regulators: C5446, C6186")
    print("  Crystals: C9002, C12674")
    print("  Connectors: C16214, C167321")
    print("  Op-Amps: C7950")
    print("  Inductors: C1017")
    print("  Switches: C318884")
    print()
    print("=" * 60)
    print("Server starting...")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
