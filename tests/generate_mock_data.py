"""
Generate large mock product database for LCSC API testing
Creates 100,000+ components with variations in manufacturers, packages, and values
"""

import random
import json

# Start with base product code counter
PRODUCT_CODE_START = 100000

def generate_resistors(start_code):
    """Generate resistor variations across manufacturers and packages."""
    manufacturers = [
        "UNI-ROYAL(Uniroyal Elec)",
        "YAGEO",
        "Vishay",
        "Panasonic",
        "KOA Speer",
        "Bourns",
        "Stackpole",
        "Rohm",
        "Samsung",
        "Walsin"
    ]
    
    # SMD packages
    smd_packages = ["0201", "0402", "0603", "0805", "1206", "1210", "2010", "2512"]
    # Through-hole packages
    axial_packages = ["Axial-0.3", "Axial-0.4", "Axial-0.6", "Axial-0.8"]
    
    # Resistance values in ohms - EXPANDED
    resistance_values = [
        (0.1, "0.1Ω"), (0.22, "0.22Ω"), (0.47, "0.47Ω"),
        (1, "1Ω"), (2.2, "2.2Ω"), (4.7, "4.7Ω"),
        (10, "10Ω"), (15, "15Ω"), (22, "22Ω"), (33, "33Ω"), (47, "47Ω"), (68, "68Ω"),
        (100, "100Ω"), (150, "150Ω"), (220, "220Ω"), (330, "330Ω"), (470, "470Ω"), (680, "680Ω"),
        (1000, "1KΩ"), (1500, "1.5KΩ"), (2200, "2.2KΩ"), (3300, "3.3KΩ"), (4700, "4.7KΩ"), (6800, "6.8KΩ"),
        (10000, "10KΩ"), (15000, "15KΩ"), (22000, "22KΩ"), (33000, "33KΩ"), (47000, "47KΩ"), (68000, "68KΩ"),
        (100000, "100KΩ"), (150000, "150KΩ"), (220000, "220KΩ"), (330000, "330KΩ"), (470000, "470KΩ"), (680000, "680KΩ"),
        (1000000, "1MΩ"), (2200000, "2.2MΩ"), (4700000, "4.7MΩ"), (10000000, "10MΩ")
    ]
    
    tolerances = ["±0.1%", "±0.5%", "±1%", "±2%", "±5%", "±10%"]
    temp_coeffs = ["±25ppm", "±50ppm", "±100ppm"]
    powers = ["1/16W", "1/10W", "1/8W", "1/4W", "1/2W", "1W"]
    
    products = {}
    code = start_code
    
    for pkg in smd_packages:
        for res_val, res_str in resistance_values:
            for tol in tolerances:
                for temp_coeff in temp_coeffs:
                    for mfr in manufacturers[:6]:  # 6 manufacturers per combo (was 5)
                        model = f"{pkg}WAF{res_val}T5E-{temp_coeff.replace('±', '')}"
                        power = "1/16W" if pkg == "0201" else "1/10W" if pkg in ["0402", "0603"] else "1/8W" if pkg == "0805" else "1/4W"
                        
                        products[f"C{code}"] = {
                            "productCode": f"C{code}",
                            "productModel": model,
                            "productName": f"RES {res_str} {tol} {power} {pkg} {temp_coeff}",
                            "productIntroEn": f"Surface mount chip resistor with {res_str} resistance, {tol} tolerance, {power} power rating in {pkg} package. Features {temp_coeff} temperature coefficient for stable performance across temperature range. Ideal for general purpose applications, signal processing, and voltage division circuits. RoHS compliant.",
                            "brandName": mfr,
                            "packageType": pkg,
                            "productUnit": "pcs",
                            "minPacketUnit": "3000" if pkg in ["0201", "0402", "0603"] else "2000",
                            "minBuyNumber": "1",
                            "stockNumber": str(random.randint(50000, 500000)),
                            "productPriceList": [
                                {"startNumber": "1", "productPrice": f"{random.uniform(0.0003, 0.002):.4f}", "discountRate": "100"},
                                {"startNumber": "10", "productPrice": f"{random.uniform(0.0002, 0.0015):.4f}", "discountRate": "100"},
                                {"startNumber": "100", "productPrice": f"{random.uniform(0.0001, 0.001):.4f}", "discountRate": "100"}
                            ],
                            "paramVOList": [
                                {"paramCode": "Resistance", "paramValue": res_str},
                                {"paramCode": "Tolerance", "paramValue": tol},
                                {"paramCode": "Power", "paramValue": power},
                                {"paramCode": "Temp Coefficient", "paramValue": temp_coeff}
                            ]
                        }
                        code += 1
    
    # Add through-hole resistors
    for pkg in axial_packages:
        for res_val, res_str in resistance_values[::2]:  # Every other value
            for power in ["1/4W", "1/2W", "1W"]:
                for mfr in manufacturers[5:8]:  # Different manufacturers for through-hole
                    model = f"{pkg}-{res_val}-{power}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"RES {res_str} ±5% {power} AXIAL",
                        "productIntroEn": f"Through-hole axial lead resistor with {res_str} resistance value and ±5% tolerance. {power} power dissipation capability in standard {pkg} package. Suitable for PCB mounting, breadboarding, and applications requiring higher power handling. Lead-free and RoHS compliant construction.",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "1000",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(10000, 100000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.002, 0.01):.4f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.0015, 0.008):.4f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.001, 0.005):.4f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Resistance", "paramValue": res_str},
                            {"paramCode": "Tolerance", "paramValue": "±5%"},
                            {"paramCode": "Power", "paramValue": power}
                        ]
                    }
                    code += 1
    
    return products, code


def generate_capacitors(start_code):
    """Generate capacitor variations across manufacturers and packages."""
    manufacturers = [
        "SAMSUNG",
        "Murata",
        "TDK",
        "YAGEO",
        "Kemet",
        "Vishay",
        "AVX",
        "Nichicon",
        "Panasonic",
        "Walsin"
    ]
    
    # SMD packages for ceramic
    smd_packages = ["0201", "0402", "0603", "0805", "1206", "1210", "1812", "2220"]
    
    # Capacitance values in pF - EXPANDED
    cap_values = [
        (1, "1pF"), (2.2, "2.2pF"), (4.7, "4.7pF"),
        (10, "10pF"), (15, "15pF"), (22, "22pF"), (33, "33pF"), (47, "47pF"), (68, "68pF"),
        (100, "100pF"), (150, "150pF"), (220, "220pF"), (330, "330pF"), (470, "470pF"), (680, "680pF"),
        (1000, "1nF"), (1500, "1.5nF"), (2200, "2.2nF"), (3300, "3.3nF"), (4700, "4.7nF"), (6800, "6.8nF"),
        (10000, "10nF"), (15000, "15nF"), (22000, "22nF"), (33000, "33nF"), (47000, "47nF"), (68000, "68nF"),
        (100000, "100nF"), (150000, "150nF"), (220000, "220nF"), (330000, "330nF"), (470000, "470nF"),
        (1000000, "1µF"), (1500000, "1.5µF"), (2200000, "2.2µF"), (3300000, "3.3µF"), (4700000, "4.7µF"),
        (10000000, "10µF"), (22000000, "22µF"), (33000000, "33µF"), (47000000, "47µF"), (100000000, "100µF")
    ]
    
    voltages = ["6.3V", "10V", "16V", "25V", "50V", "100V"]
    dielectrics = ["C0G/NP0", "X5R", "X7R", "Y5V"]
    
    products = {}
    code = start_code
    
    for pkg in smd_packages:
        for cap_val, cap_str in cap_values:
            for volt in voltages:  # Use ALL voltages
                for diel in dielectrics:  # Use ALL dielectrics
                    for mfr in manufacturers[:6]:  # Use 6 manufacturers
                        model = f"CL{pkg[1:]}{cap_val}K{volt[0]}"
                        
                        products[f"C{code}"] = {
                            "productCode": f"C{code}",
                            "productModel": model,
                            "productName": f"CAP CER {cap_str} {volt} {diel} {pkg}",
                            "productIntroEn": f"Multilayer ceramic chip capacitor (MLCC) with {cap_str} capacitance rated at {volt}. {diel} dielectric material provides excellent stability and reliability. {pkg} SMD package for automatic assembly. Ideal for decoupling, filtering, and energy storage in power supplies and digital circuits. Automotive grade available, RoHS compliant.",
                            "brandName": mfr,
                            "packageType": pkg,
                            "productUnit": "pcs",
                            "minPacketUnit": "4000" if pkg in ["0201", "0402", "0603"] else "2000",
                            "minBuyNumber": "1",
                            "stockNumber": str(random.randint(80000, 600000)),
                            "productPriceList": [
                                {"startNumber": "1", "productPrice": f"{random.uniform(0.003, 0.05):.4f}", "discountRate": "100"},
                                {"startNumber": "10", "productPrice": f"{random.uniform(0.002, 0.04):.4f}", "discountRate": "100"},
                                {"startNumber": "100", "productPrice": f"{random.uniform(0.001, 0.03):.4f}", "discountRate": "100"}
                            ],
                            "paramVOList": [
                                {"paramCode": "Capacitance", "paramValue": cap_str},
                                {"paramCode": "Voltage", "paramValue": volt},
                                {"paramCode": "Tolerance", "paramValue": "±10%"},
                                {"paramCode": "Dielectric", "paramValue": diel}
                            ]
                        }
                        code += 1
    
    # Add electrolytic capacitors
    elec_packages = ["D5xL11mm", "D6.3xL5mm", "D8xL10mm", "D10xL13mm", "D12.5xL20mm"]
    elec_caps = [(1, "1µF"), (10, "10µF"), (22, "22µF"), (47, "47µF"), (100, "100µF"), 
                 (220, "220µF"), (470, "470µF"), (1000, "1000µF"), (2200, "2200µF")]
    elec_volts = ["6.3V", "10V", "16V", "25V", "35V", "50V", "63V"]
    
    for pkg in elec_packages:
        for cap_val, cap_str in elec_caps:
            for volt in elec_volts:
                for mfr in manufacturers[6:9]:
                    model = f"CA{volt.replace('.', '')}M{cap_val}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"CAP ALUM {cap_str} {volt} 20% RADIAL",
                        "brandName": mfr,
                        "packageType": f"Plugin,{pkg}",
                        "productUnit": "pcs",
                        "minPacketUnit": "1000",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(5000, 80000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.02, 0.15):.4f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.015, 0.12):.4f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.01, 0.09):.4f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Capacitance", "paramValue": cap_str},
                            {"paramCode": "Voltage", "paramValue": volt},
                            {"paramCode": "Tolerance", "paramValue": "±20%"},
                            {"paramCode": "Type", "paramValue": "Electrolytic"}
                        ]
                    }
                    code += 1
    
    return products, code


def generate_inductors(start_code):
    """Generate inductor variations across manufacturers and packages."""
    manufacturers = [
        "Sunlord",
        "Murata",
        "TDK",
        "Bourns",
        "Coilcraft",
        "Taiyo Yuden",
        "Wurth Elektronik",
        "Vishay"
    ]
    
    smd_packages = ["0402", "0603", "0805", "1206", "1210", "1812"]
    axial_packages = ["Axial-0.4", "Axial-0.6"]
    
    # Inductance values in µH - EXPANDED
    ind_values = [
        (0.01, "10nH"), (0.022, "22nH"), (0.047, "47nH"),
        (0.1, "100nH"), (0.15, "150nH"), (0.22, "220nH"), (0.33, "330nH"), (0.47, "470nH"), (0.68, "680nH"),
        (1, "1µH"), (1.5, "1.5µH"), (2.2, "2.2µH"), (3.3, "3.3µH"), (4.7, "4.7µH"), (6.8, "6.8µH"),
        (10, "10µH"), (15, "15µH"), (22, "22µH"), (33, "33µH"), (47, "47µH"), (68, "68µH"),
        (100, "100µH"), (150, "150µH"), (220, "220µH"), (330, "330µH"), (470, "470µH"), (680, "680µH"),
        (1000, "1mH"), (1500, "1.5mH"), (2200, "2.2mH"), (3300, "3.3mH"), (4700, "4.7mH"),
        (10000, "10mH")
    ]
    
    currents = ["100mA", "200mA", "300mA", "500mA", "1A", "2A", "3A"]
    
    products = {}
    code = start_code
    
    for pkg in smd_packages:
        for ind_val, ind_str in ind_values:
            for curr in currents:  # Use ALL current ratings
                for mfr in manufacturers[:6]:  # Use 6 manufacturers
                    model = f"SDFL{pkg[1:]}{int(ind_val*10)}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"INDUCTOR {ind_str} 20% {curr} {pkg}",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "3000",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(30000, 200000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.01, 0.08):.4f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.008, 0.06):.4f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.005, 0.04):.4f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Inductance", "paramValue": ind_str},
                            {"paramCode": "Tolerance", "paramValue": "±20%"},
                            {"paramCode": "Current", "paramValue": curr},
                            {"paramCode": "DCR", "paramValue": f"{random.uniform(0.1, 5):.1f}Ω"}
                        ]
                    }
                    code += 1
    
    # Add axial inductors
    for pkg in axial_packages:
        for ind_val, ind_str in ind_values[5::2]:
            for curr in currents[3:]:
                for mfr in manufacturers[4:7]:
                    model = f"{pkg}-{int(ind_val)}uH-{curr}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"INDUCTOR {ind_str} 10% {curr} AXIAL",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "1000",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(5000, 50000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.05, 0.3):.4f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.04, 0.25):.4f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.03, 0.2):.4f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Inductance", "paramValue": ind_str},
                            {"paramCode": "Tolerance", "paramValue": "±10%"},
                            {"paramCode": "Current", "paramValue": curr}
                        ]
                    }
                    code += 1
    
    return products, code


def generate_crystals(start_code):
    """Generate crystal and oscillator variations."""
    manufacturers = [
        "Yangxing Tech",
        "Epson",
        "TXC",
        "Abracon",
        "Kyocera AVX",
        "NDK",
        "Seiko Instruments"
    ]
    
    smd_packages = ["HC-49S-SMD", "2P-3.2x2.5mm", "2P-5.0x3.2mm", "2P-6.0x3.5mm", "4P-5.0x3.2mm"]
    through_hole_packages = ["HC-49S", "HC-49U"]
    
    # Crystal frequencies in Hz - EXPANDED
    frequencies = [
        (32768, "32.768kHz"),
        (1000000, "1MHz"), (1843200, "1.8432MHz"), (2000000, "2MHz"),
        (3579545, "3.579545MHz"), (4000000, "4MHz"), (6000000, "6MHz"),
        (8000000, "8MHz"), (10000000, "10MHz"), (11059200, "11.0592MHz"),
        (12000000, "12MHz"), (14318180, "14.31818MHz"), (16000000, "16MHz"),
        (18432000, "18.432MHz"), (20000000, "20MHz"), (22118400, "22.1184MHz"),
        (24000000, "24MHz"), (25000000, "25MHz"), (26000000, "26MHz"),
        (27000000, "27MHz"), (30000000, "30MHz"), (32000000, "32MHz"),
        (33333000, "33.333MHz"), (40000000, "40MHz"), (48000000, "48MHz"),
        (50000000, "50MHz"), (60000000, "60MHz"), (66666000, "66.666MHz"),
        (72000000, "72MHz"), (80000000, "80MHz"), (100000000, "100MHz")
    ]
    
    load_caps = ["8pF", "10pF", "12.5pF", "15pF", "18pF", "20pF"]
    
    products = {}
    code = start_code
    
    for pkg in smd_packages:
        for freq_val, freq_str in frequencies:
            for cap in load_caps:  # Use ALL load capacitances
                for mfr in manufacturers:  # Use ALL manufacturers
                    model = f"X{pkg[:2]}{freq_val//1000}K{cap[:2]}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"CRYSTAL {freq_str} {cap} SMD",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "1000" if freq_val == 32768 else "3000",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(20000, 150000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.05, 0.3):.4f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.04, 0.25):.4f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.03, 0.2):.4f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Frequency", "paramValue": freq_str},
                            {"paramCode": "Load Capacitance", "paramValue": cap},
                            {"paramCode": "Tolerance", "paramValue": "±20ppm"},
                            {"paramCode": "Operating Temperature", "paramValue": "-20°C ~ 70°C"}
                        ]
                    }
                    code += 1
    
    # Through-hole crystals
    for pkg in through_hole_packages:
        for freq_val, freq_str in frequencies[2::2]:
            for cap in load_caps[1::2]:
                for mfr in manufacturers[3:6]:
                    model = f"{pkg}-{freq_val//1000000}MHz-{cap}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"CRYSTAL {freq_str} {cap} THROUGH-HOLE",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "500",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(5000, 50000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.08, 0.4):.4f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.06, 0.35):.4f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.05, 0.3):.4f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Frequency", "paramValue": freq_str},
                            {"paramCode": "Load Capacitance", "paramValue": cap},
                            {"paramCode": "Tolerance", "paramValue": "±30ppm"}
                        ]
                    }
                    code += 1
    
    return products, code


def generate_ics(start_code):
    """Generate IC variations across manufacturers and types."""
    manufacturers = [
        "STMicroelectronics",
        "Texas Instruments",
        "Analog Devices",
        "Microchip",
        "NXP",
        "Infineon",
        "ON Semiconductor",
        "Renesas",
        "Maxim Integrated",
        "Silicon Labs"
    ]
    
    # Microcontrollers
    mcu_families = [
        ("STM32F0", "ARM Cortex-M0", ["LQFP32", "LQFP48", "LQFP64"], ["16KB", "32KB", "64KB"], ["4KB", "8KB", "16KB"], "48MHz"),
        ("STM32F1", "ARM Cortex-M3", ["LQFP48", "LQFP64", "LQFP100"], ["64KB", "128KB", "256KB"], ["20KB", "48KB", "64KB"], "72MHz"),
        ("STM32F4", "ARM Cortex-M4", ["LQFP64", "LQFP100", "LQFP144"], ["256KB", "512KB", "1MB"], ["128KB", "192KB", "256KB"], "168MHz"),
        ("ATMEGA", "AVR", ["DIP28", "TQFP32", "TQFP44"], ["8KB", "16KB", "32KB"], ["1KB", "2KB", "4KB"], "16MHz"),
        ("PIC16F", "PIC", ["DIP18", "SOIC20", "TQFP28"], ["4KB", "8KB", "14KB"], ["256B", "512B", "1KB"], "32MHz"),
        ("ESP32", "Xtensa LX6", ["QFN48", "QFN56"], ["4MB", "8MB", "16MB"], ["520KB"], "240MHz"),
        ("NRF52", "ARM Cortex-M4", ["QFN48", "QFN52"], ["256KB", "512KB", "1MB"], ["32KB", "64KB", "256KB"], "64MHz")
    ]
    
    # Op-Amps and Comparators
    opamp_types = [
        ("Single", ["SOT23-5", "SOIC-8", "DIP-8"], "1", ["1MHz", "10MHz", "100MHz"]),
        ("Dual", ["SOIC-8", "DIP-8", "MSOP-8"], "2", ["700kHz", "5MHz", "50MHz"]),
        ("Quad", ["SOIC-14", "DIP-14", "TSSOP-14"], "4", ["1MHz", "10MHz", "40MHz"])
    ]
    
    # Voltage Regulators
    regulator_types = [
        ("LDO", ["SOT23-5", "SOT89", "SOT223", "TO-252"], ["1.8V", "2.5V", "3.3V", "5.0V", "12V"], ["100mA", "500mA", "1A", "3A"]),
        ("Buck", ["SOIC-8", "MSOP-8", "QFN-16"], ["3.3V", "5V", "12V", "Adjustable"], ["1A", "2A", "3A", "5A"]),
        ("Boost", ["SOT23-6", "SOIC-8"], ["5V", "12V", "Adjustable"], ["500mA", "1A", "2A"])
    ]
    
    # Interface ICs
    interface_types = [
        ("RS232", ["SOIC-16", "DIP-16", "TSSOP-16"], ["1", "2", "4"], "±15V"),
        ("RS485", ["SOIC-8", "DIP-8", "MSOP-8"], ["1", "2"], "±7V"),
        ("CAN", ["SOIC-8", "DIP-8"], ["1"], "5V"),
        ("USB", ["SOIC-16", "TSSOP-20", "QFN-28"], ["1", "2", "4"], "5V"),
        ("I2C", ["SOT23-6", "SOIC-8", "MSOP-8"], ["1", "2"], "5V"),
        ("SPI", ["SOIC-8", "MSOP-8"], ["1"], "5V")
    ]
    
    products = {}
    code = start_code
    
    # Generate Microcontrollers
    for family, core, packages, flash_sizes, ram_sizes, speed in mcu_families:
        for pkg in packages:
            for flash in flash_sizes:
                for ram in ram_sizes:
                    for mfr in manufacturers[:3]:
                        model = f"{family}{flash[:2]}{pkg[:4]}"
                        
                        products[f"C{code}"] = {
                            "productCode": f"C{code}",
                            "productModel": model,
                            "productName": f"MCU {core} {flash} FLASH {ram} RAM {pkg}",
                            "brandName": mfr,
                            "packageType": pkg,
                            "productUnit": "pcs",
                            "minPacketUnit": "1",
                            "minBuyNumber": "1",
                            "stockNumber": str(random.randint(1000, 50000)),
                            "productPriceList": [
                                {"startNumber": "1", "productPrice": f"{random.uniform(1.5, 15):.2f}", "discountRate": "100"},
                                {"startNumber": "10", "productPrice": f"{random.uniform(1.2, 12):.2f}", "discountRate": "100"},
                                {"startNumber": "100", "productPrice": f"{random.uniform(0.8, 8):.2f}", "discountRate": "100"}
                            ],
                            "paramVOList": [
                                {"paramCode": "Core", "paramValue": core},
                                {"paramCode": "Flash", "paramValue": flash},
                                {"paramCode": "RAM", "paramValue": ram},
                                {"paramCode": "Speed", "paramValue": speed},
                                {"paramCode": "Package", "paramValue": pkg}
                            ]
                        }
                        code += 1
    
    # Generate Op-Amps
    for opamp_type, packages, channels, bandwidths in opamp_types:
        for pkg in packages:
            for bw in bandwidths:
                for mfr in manufacturers[1:5]:
                    model = f"LM{random.randint(100, 999)}{pkg[:3]}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"OP-AMP {opamp_type} {bw} {pkg}",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "50",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(10000, 100000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.1, 2):.2f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.08, 1.5):.2f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.05, 1):.2f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Type", "paramValue": opamp_type},
                            {"paramCode": "Channels", "paramValue": channels},
                            {"paramCode": "Bandwidth", "paramValue": bw},
                            {"paramCode": "Package", "paramValue": pkg}
                        ]
                    }
                    code += 1
    
    # Generate Voltage Regulators
    for reg_type, packages, voltages, currents in regulator_types:
        for pkg in packages:
            for volt in voltages:
                for curr in currents:
                    for mfr in manufacturers[2:6]:
                        model = f"{reg_type}{volt.replace('.', '')}-{curr}"
                        
                        products[f"C{code}"] = {
                            "productCode": f"C{code}",
                            "productModel": model,
                            "productName": f"REGULATOR {reg_type} {volt} {curr} {pkg}",
                            "brandName": mfr,
                            "packageType": pkg,
                            "productUnit": "pcs",
                            "minPacketUnit": "50",
                            "minBuyNumber": "1",
                            "stockNumber": str(random.randint(5000, 80000)),
                            "productPriceList": [
                                {"startNumber": "1", "productPrice": f"{random.uniform(0.2, 3):.2f}", "discountRate": "100"},
                                {"startNumber": "10", "productPrice": f"{random.uniform(0.15, 2.5):.2f}", "discountRate": "100"},
                                {"startNumber": "100", "productPrice": f"{random.uniform(0.1, 2):.2f}", "discountRate": "100"}
                            ],
                            "paramVOList": [
                                {"paramCode": "Type", "paramValue": reg_type},
                                {"paramCode": "Output Voltage", "paramValue": volt},
                                {"paramCode": "Current", "paramValue": curr},
                                {"paramCode": "Package", "paramValue": pkg}
                            ]
                        }
                        code += 1
    
    # Generate Interface ICs
    for ifc_type, packages, channels_list, voltage in interface_types:
        for pkg in packages:
            for channels in channels_list:
                for mfr in manufacturers[3:7]:
                    model = f"MAX{random.randint(100, 999)}{ifc_type[:3]}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"INTERFACE {ifc_type} {channels}CH {pkg}",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "50",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(8000, 60000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.3, 4):.2f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.25, 3):.2f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.15, 2):.2f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Type", "paramValue": ifc_type},
                            {"paramCode": "Channels", "paramValue": channels},
                            {"paramCode": "Voltage", "paramValue": voltage},
                            {"paramCode": "Package", "paramValue": pkg}
                        ]
                    }
                    code += 1
    
    return products, code


def generate_sensors(start_code):
    """Generate sensor variations across manufacturers and types."""
    manufacturers = [
        "Bosch",
        "STMicroelectronics",
        "Analog Devices",
        "Texas Instruments",
        "Honeywell",
        "TE Connectivity",
        "Sensirion",
        "InvenSense",
        "Melexis",
        "AMS"
    ]
    
    # Temperature Sensors
    temp_sensor_types = [
        ("Analog", ["SOT23-3", "TO-92", "SOIC-8"], ["-40°C ~ 125°C", "-55°C ~ 150°C"], ["±0.5°C", "±1°C", "±2°C"]),
        ("Digital I2C", ["SOT23-6", "DFN-6", "SOIC-8"], ["-40°C ~ 125°C", "-55°C ~ 150°C"], ["±0.25°C", "±0.5°C"]),
        ("Digital SPI", ["SOIC-8", "DFN-8"], ["-40°C ~ 125°C"], ["±0.1°C", "±0.25°C"])
    ]
    
    # Pressure Sensors
    pressure_ranges = ["100kPa", "200kPa", "300kPa", "500kPa", "1MPa", "5MPa", "10MPa"]
    pressure_packages = ["DIP-8", "SOIC-8", "LGA-8", "QFN-12"]
    
    # Humidity Sensors
    humidity_types = [
        ("Capacitive", ["DFN-4", "DFN-6", "LGA-6"], ["0-100%RH"], ["±2%", "±3%"]),
        ("Resistive", ["SOIC-8", "DIP-8"], ["0-100%RH"], ["±3%", "±5%"])
    ]
    
    # Motion Sensors (Accelerometer, Gyro, IMU)
    motion_types = [
        ("Accelerometer 3-Axis", ["LGA-12", "LGA-14", "QFN-16"], ["±2g", "±4g", "±8g", "±16g"]),
        ("Gyroscope 3-Axis", ["LGA-16", "QFN-16", "QFN-24"], ["±250°/s", "±500°/s", "±1000°/s", "±2000°/s"]),
        ("IMU 6-Axis", ["LGA-14", "QFN-24"], ["±2g/±250°/s", "±16g/±2000°/s"])
    ]
    
    # Magnetic Sensors
    magnetic_types = [
        ("Hall Effect", ["SOT23-3", "TO-92", "SOIC-8"], ["Unipolar", "Bipolar", "Latch"]),
        ("Magnetometer 3-Axis", ["LGA-12", "QFN-16"], ["±4 gauss", "±8 gauss", "±12 gauss"])
    ]
    
    # Light Sensors
    light_types = [
        ("Ambient Light", ["DFN-6", "SOIC-8"], ["Analog", "Digital I2C"]),
        ("Proximity", ["DFN-6", "LGA-8"], ["I2C", "Analog"]),
        ("Color", ["DFN-6", "LGA-10"], ["RGB", "RGBW", "RGB+IR"])
    ]
    
    products = {}
    code = start_code
    
    # Generate Temperature Sensors
    for sensor_type, packages, temp_ranges, accuracies in temp_sensor_types:
        for pkg in packages:
            for temp_range in temp_ranges:
                for accuracy in accuracies:
                    for mfr in manufacturers[:4]:
                        model = f"TMP{random.randint(100, 999)}{pkg[:3]}"
                        
                        products[f"C{code}"] = {
                            "productCode": f"C{code}",
                            "productModel": model,
                            "productName": f"TEMP SENSOR {sensor_type} {temp_range} {accuracy} {pkg}",
                            "brandName": mfr,
                            "packageType": pkg,
                            "productUnit": "pcs",
                            "minPacketUnit": "50",
                            "minBuyNumber": "1",
                            "stockNumber": str(random.randint(5000, 50000)),
                            "productPriceList": [
                                {"startNumber": "1", "productPrice": f"{random.uniform(0.3, 3):.2f}", "discountRate": "100"},
                                {"startNumber": "10", "productPrice": f"{random.uniform(0.25, 2.5):.2f}", "discountRate": "100"},
                                {"startNumber": "100", "productPrice": f"{random.uniform(0.15, 2):.2f}", "discountRate": "100"}
                            ],
                            "paramVOList": [
                                {"paramCode": "Type", "paramValue": sensor_type},
                                {"paramCode": "Temperature Range", "paramValue": temp_range},
                                {"paramCode": "Accuracy", "paramValue": accuracy},
                                {"paramCode": "Package", "paramValue": pkg}
                            ]
                        }
                        code += 1
    
    # Generate Pressure Sensors
    for press_range in pressure_ranges:
        for pkg in pressure_packages:
            for mfr in manufacturers[3:7]:
                model = f"MPX{press_range[:3]}{pkg[:3]}"
                
                products[f"C{code}"] = {
                    "productCode": f"C{code}",
                    "productModel": model,
                    "productName": f"PRESSURE SENSOR {press_range} {pkg}",
                    "brandName": mfr,
                    "packageType": pkg,
                    "productUnit": "pcs",
                    "minPacketUnit": "25",
                    "minBuyNumber": "1",
                    "stockNumber": str(random.randint(2000, 20000)),
                    "productPriceList": [
                        {"startNumber": "1", "productPrice": f"{random.uniform(2, 15):.2f}", "discountRate": "100"},
                        {"startNumber": "10", "productPrice": f"{random.uniform(1.5, 12):.2f}", "discountRate": "100"},
                        {"startNumber": "100", "productPrice": f"{random.uniform(1, 10):.2f}", "discountRate": "100"}
                    ],
                    "paramVOList": [
                        {"paramCode": "Type", "paramValue": "Pressure"},
                        {"paramCode": "Range", "paramValue": press_range},
                        {"paramCode": "Output", "paramValue": "Analog"},
                        {"paramCode": "Package", "paramValue": pkg}
                    ]
                }
                code += 1
    
    # Generate Humidity Sensors
    for humid_type, packages, ranges, accuracies in humidity_types:
        for pkg in packages:
            for accuracy in accuracies:
                for mfr in manufacturers[5:9]:
                    model = f"SHT{random.randint(10, 99)}{pkg[:3]}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"HUMIDITY SENSOR {humid_type} {accuracy} {pkg}",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "50",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(3000, 30000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(1, 8):.2f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.8, 6):.2f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.5, 4):.2f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Type", "paramValue": humid_type},
                            {"paramCode": "Range", "paramValue": ranges[0]},
                            {"paramCode": "Accuracy", "paramValue": accuracy},
                            {"paramCode": "Package", "paramValue": pkg}
                        ]
                    }
                    code += 1
    
    # Generate Motion Sensors
    for motion_type, packages, ranges in motion_types:
        for pkg in packages:
            for range_val in ranges:
                for mfr in manufacturers[6:10]:
                    model = f"LSM{random.randint(100, 999)}{pkg[:3]}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"MOTION SENSOR {motion_type} {range_val} {pkg}",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "50",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(5000, 40000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(1.5, 10):.2f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(1.2, 8):.2f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.8, 6):.2f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Type", "paramValue": motion_type},
                            {"paramCode": "Range", "paramValue": range_val},
                            {"paramCode": "Interface", "paramValue": "I2C/SPI"},
                            {"paramCode": "Package", "paramValue": pkg}
                        ]
                    }
                    code += 1
    
    # Generate Magnetic Sensors
    for mag_type, packages, options in magnetic_types:
        for pkg in packages:
            for option in options:
                for mfr in manufacturers[1:5]:
                    model = f"MAG{random.randint(100, 999)}{pkg[:3]}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"MAGNETIC SENSOR {mag_type} {option} {pkg}",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "50",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(8000, 60000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.5, 5):.2f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.4, 4):.2f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.2, 3):.2f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Type", "paramValue": mag_type},
                            {"paramCode": "Mode", "paramValue": option},
                            {"paramCode": "Package", "paramValue": pkg}
                        ]
                    }
                    code += 1
    
    # Generate Light Sensors
    for light_type, packages, interfaces in light_types:
        for pkg in packages:
            for interface in interfaces:
                for mfr in manufacturers[2:6]:
                    model = f"OPT{random.randint(100, 999)}{pkg[:3]}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"LIGHT SENSOR {light_type} {interface} {pkg}",
                        "brandName": mfr,
                        "packageType": pkg,
                        "productUnit": "pcs",
                        "minPacketUnit": "50",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(6000, 50000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.5, 4):.2f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.4, 3):.2f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.25, 2):.2f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Type", "paramValue": light_type},
                            {"paramCode": "Interface", "paramValue": interface},
                            {"paramCode": "Package", "paramValue": pkg}
                        ]
                    }
                    code += 1
    
    return products, code


def generate_connectors(start_code):
    """Generate connector variations across manufacturers and types."""
    manufacturers = [
        "Molex",
        "TE Connectivity",
        "JST",
        "Amphenol",
        "Hirose",
        "JAE",
        "Samtec",
        "Wurth Elektronik",
        "Korean Hroparts Elec",
        "SHOU HAN"
    ]
    
    # Pin Headers
    header_pins = ["2", "3", "4", "5", "6", "8", "10", "12", "16", "20", "24", "32", "40"]
    header_pitches = ["1.27mm", "2.0mm", "2.54mm"]
    header_orientations = ["Straight", "Right Angle"]
    header_types = ["Male", "Female"]
    
    # USB Connectors
    usb_types = [
        ("USB Type-A", ["SMD", "Through-Hole"], ["Receptacle", "Plug"], ["Right Angle", "Straight"]),
        ("USB Type-B", ["SMD", "Through-Hole"], ["Receptacle", "Plug"], ["Right Angle", "Straight"]),
        ("USB Type-C", ["SMD"], ["Receptacle", "Plug"], ["Right Angle", "Straight", "Mid-Mount"]),
        ("USB Micro-B", ["SMD"], ["Receptacle"], ["Right Angle", "Straight"]),
        ("USB Mini-B", ["SMD", "Through-Hole"], ["Receptacle"], ["Right Angle", "Straight"])
    ]
    
    # Card Connectors
    card_types = [
        ("SD Card", ["SMD", "Through-Hole"], ["Push-Push", "Hinge", "Drawer"]),
        ("Micro SD", ["SMD"], ["Push-Push", "Hinge"]),
        ("SIM Card", ["SMD"], ["Push-Push", "Drawer"])
    ]
    
    # Wire-to-Board
    wtb_pins = ["2", "3", "4", "5", "6", "8", "10", "12"]
    wtb_pitches = ["2.0mm", "2.5mm", "3.96mm", "5.08mm"]
    wtb_types = ["Terminal Block", "Spring Terminal", "Screw Terminal"]
    
    # Board-to-Board
    btb_pins = ["10", "20", "30", "40", "50", "60", "80", "100"]
    btb_pitches = ["0.4mm", "0.5mm", "0.8mm", "1.0mm", "1.27mm", "2.0mm"]
    btb_heights = ["1.5mm", "2.0mm", "3.0mm", "5.0mm", "8.0mm"]
    
    # RF Connectors
    rf_types = ["SMA", "SMB", "U.FL", "MMCX", "MCX"]
    rf_mounting = ["SMD", "Through-Hole", "Edge Mount"]
    
    products = {}
    code = start_code
    
    # Generate Pin Headers
    for pins in header_pins:
        for pitch in header_pitches:
            for orientation in header_orientations:
                for header_type in header_types:
                    for mfr in manufacturers[:4]:
                        model = f"PH{pins}P{pitch.replace('mm', '')}-{orientation[:1]}{header_type[:1]}"
                        mount = "Through-Hole" if pitch == "2.54mm" else "SMD"
                        
                        products[f"C{code}"] = {
                            "productCode": f"C{code}",
                            "productModel": model,
                            "productName": f"HEADER {header_type} {pins}P {pitch} {orientation} {mount}",
                            "brandName": mfr,
                            "packageType": f"{pins}P-{pitch}-{mount}",
                            "productUnit": "pcs",
                            "minPacketUnit": "50",
                            "minBuyNumber": "1",
                            "stockNumber": str(random.randint(10000, 100000)),
                            "productPriceList": [
                                {"startNumber": "1", "productPrice": f"{random.uniform(0.05, 1):.2f}", "discountRate": "100"},
                                {"startNumber": "10", "productPrice": f"{random.uniform(0.04, 0.8):.2f}", "discountRate": "100"},
                                {"startNumber": "100", "productPrice": f"{random.uniform(0.02, 0.5):.2f}", "discountRate": "100"}
                            ],
                            "paramVOList": [
                                {"paramCode": "Type", "paramValue": header_type},
                                {"paramCode": "Pins", "paramValue": pins},
                                {"paramCode": "Pitch", "paramValue": pitch},
                                {"paramCode": "Orientation", "paramValue": orientation}
                            ]
                        }
                        code += 1
    
    # Generate USB Connectors
    for usb_type, mountings, genders, orientations in usb_types:
        for mounting in mountings:
            for gender in genders:
                for orientation in orientations:
                    for mfr in manufacturers[4:8]:
                        model = f"USB-{usb_type.split()[-1]}-{gender[:1]}-{orientation[:2]}"
                        
                        products[f"C{code}"] = {
                            "productCode": f"C{code}",
                            "productModel": model,
                            "productName": f"{usb_type} {gender} {orientation} {mounting}",
                            "brandName": mfr,
                            "packageType": mounting,
                            "productUnit": "pcs",
                            "minPacketUnit": "50",
                            "minBuyNumber": "1",
                            "stockNumber": str(random.randint(5000, 80000)),
                            "productPriceList": [
                                {"startNumber": "1", "productPrice": f"{random.uniform(0.15, 2):.2f}", "discountRate": "100"},
                                {"startNumber": "10", "productPrice": f"{random.uniform(0.12, 1.5):.2f}", "discountRate": "100"},
                                {"startNumber": "100", "productPrice": f"{random.uniform(0.08, 1):.2f}", "discountRate": "100"}
                            ],
                            "paramVOList": [
                                {"paramCode": "Type", "paramValue": usb_type},
                                {"paramCode": "Gender", "paramValue": gender},
                                {"paramCode": "Orientation", "paramValue": orientation},
                                {"paramCode": "Mounting", "paramValue": mounting}
                            ]
                        }
                        code += 1
    
    # Generate Card Connectors
    for card_type, mountings, mechanisms in card_types:
        for mounting in mountings:
            for mechanism in mechanisms:
                for mfr in manufacturers[2:6]:
                    model = f"{card_type.replace(' ', '')}-{mechanism[:2]}-{mounting[:3]}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"{card_type} CONNECTOR {mechanism} {mounting}",
                        "brandName": mfr,
                        "packageType": mounting,
                        "productUnit": "pcs",
                        "minPacketUnit": "25",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(3000, 50000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.3, 3):.2f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.25, 2.5):.2f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.15, 2):.2f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Type", "paramValue": card_type},
                            {"paramCode": "Mechanism", "paramValue": mechanism},
                            {"paramCode": "Mounting", "paramValue": mounting}
                        ]
                    }
                    code += 1
    
    # Generate Wire-to-Board
    for pins in wtb_pins:
        for pitch in wtb_pitches:
            for wtb_type in wtb_types:
                for mfr in manufacturers[6:10]:
                    model = f"WTB{pins}P-{pitch.replace('mm', '')}-{wtb_type[:3]}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"{wtb_type} {pins}P {pitch}",
                        "brandName": mfr,
                        "packageType": f"Through-Hole-{pitch}",
                        "productUnit": "pcs",
                        "minPacketUnit": "50",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(5000, 60000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.1, 2):.2f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.08, 1.5):.2f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.05, 1):.2f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Type", "paramValue": wtb_type},
                            {"paramCode": "Pins", "paramValue": pins},
                            {"paramCode": "Pitch", "paramValue": pitch}
                        ]
                    }
                    code += 1
    
    # Generate Board-to-Board
    for pins in btb_pins:
        for pitch in btb_pitches:
            for height in btb_heights:
                for mfr in manufacturers[1:5]:
                    model = f"BTB{pins}P-{pitch.replace('mm', '')}-{height.replace('mm', 'H')}"
                    
                    products[f"C{code}"] = {
                        "productCode": f"C{code}",
                        "productModel": model,
                        "productName": f"BOARD-TO-BOARD {pins}P {pitch} {height} SMD",
                        "brandName": mfr,
                        "packageType": f"SMD-{pitch}-{height}",
                        "productUnit": "pcs",
                        "minPacketUnit": "50",
                        "minBuyNumber": "1",
                        "stockNumber": str(random.randint(3000, 40000)),
                        "productPriceList": [
                            {"startNumber": "1", "productPrice": f"{random.uniform(0.2, 4):.2f}", "discountRate": "100"},
                            {"startNumber": "10", "productPrice": f"{random.uniform(0.15, 3):.2f}", "discountRate": "100"},
                            {"startNumber": "100", "productPrice": f"{random.uniform(0.1, 2):.2f}", "discountRate": "100"}
                        ],
                        "paramVOList": [
                            {"paramCode": "Type", "paramValue": "Board-to-Board"},
                            {"paramCode": "Pins", "paramValue": pins},
                            {"paramCode": "Pitch", "paramValue": pitch},
                            {"paramCode": "Height", "paramValue": height}
                        ]
                    }
                    code += 1
    
    # Generate RF Connectors
    for rf_type in rf_types:
        for mounting in rf_mounting:
            for mfr in manufacturers[3:7]:
                model = f"{rf_type}-{mounting[:3]}"
                
                products[f"C{code}"] = {
                    "productCode": f"C{code}",
                    "productModel": model,
                    "productName": f"RF CONNECTOR {rf_type} {mounting}",
                    "brandName": mfr,
                    "packageType": mounting,
                    "productUnit": "pcs",
                    "minPacketUnit": "25",
                    "minBuyNumber": "1",
                    "stockNumber": str(random.randint(2000, 30000)),
                    "productPriceList": [
                        {"startNumber": "1", "productPrice": f"{random.uniform(0.5, 5):.2f}", "discountRate": "100"},
                        {"startNumber": "10", "productPrice": f"{random.uniform(0.4, 4):.2f}", "discountRate": "100"},
                        {"startNumber": "100", "productPrice": f"{random.uniform(0.25, 3):.2f}", "discountRate": "100"}
                    ],
                    "paramVOList": [
                        {"paramCode": "Type", "paramValue": rf_type},
                        {"paramCode": "Mounting", "paramValue": mounting},
                        {"paramCode": "Impedance", "paramValue": "50Ω"}
                    ]
                }
                code += 1
    
    return products, code


def generate_all_products():
    """Generate all mock products."""
    print("Generating mock product database...")
    print("=" * 60)
    
    all_products = {}
    current_code = PRODUCT_CODE_START
    
    print(f"Generating resistors starting at C{current_code}...")
    resistors, current_code = generate_resistors(current_code)
    all_products.update(resistors)
    print(f"  Generated {len(resistors)} resistors")
    
    print(f"Generating capacitors starting at C{current_code}...")
    capacitors, current_code = generate_capacitors(current_code)
    all_products.update(capacitors)
    print(f"  Generated {len(capacitors)} capacitors")
    
    print(f"Generating inductors starting at C{current_code}...")
    inductors, current_code = generate_inductors(current_code)
    all_products.update(inductors)
    print(f"  Generated {len(inductors)} inductors")
    
    print(f"Generating crystals starting at C{current_code}...")
    crystals, current_code = generate_crystals(current_code)
    all_products.update(crystals)
    print(f"  Generated {len(crystals)} crystals")
    
    print(f"Generating ICs starting at C{current_code}...")
    ics, current_code = generate_ics(current_code)
    all_products.update(ics)
    print(f"  Generated {len(ics)} ICs")
    
    print(f"Generating sensors starting at C{current_code}...")
    sensors, current_code = generate_sensors(current_code)
    all_products.update(sensors)
    print(f"  Generated {len(sensors)} sensors")
    
    print(f"Generating connectors starting at C{current_code}...")
    connectors, current_code = generate_connectors(current_code)
    all_products.update(connectors)
    print(f"  Generated {len(connectors)} connectors")
    
    print("=" * 60)
    print(f"Total products generated: {len(all_products)}")
    print(f"Product codes: C{PRODUCT_CODE_START} to C{current_code-1}")
    
    return all_products


if __name__ == "__main__":
    products = generate_all_products()
    
    # Save to file
    output_file = "mock_products_large.json"
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(products, f, indent=2)
    print(f"Saved {len(products)} products to {output_file}")
    print(f"File size: {len(json.dumps(products)) / 1024 / 1024:.2f} MB")
