"""
Add product descriptions to existing mock_products_large.json
"""

import json
import re

def generate_description(product):
    """Generate a detailed description based on product data."""
    name = product.get('productName', '')
    model = product.get('productModel', '')
    brand = product.get('brandName', '')
    package = product.get('packageType', '')
    params = product.get('paramVOList', [])
    
    # Extract key parameters
    param_dict = {p['paramCode']: p['paramValue'] for p in params}
    
    # Detect component type from name
    name_upper = name.upper()
    
    if 'RES' in name_upper or 'RESISTOR' in name_upper:
        resistance = param_dict.get('Resistance', '')
        tolerance = param_dict.get('Tolerance', '±5%')
        power = param_dict.get('Power', '')
        temp_coeff = param_dict.get('Temp Coefficient', '±100ppm')
        
        if 'AXIAL' in name_upper:
            return f"Through-hole axial lead resistor featuring {resistance} resistance value with {tolerance} tolerance. {power} power dissipation capability in standard {package} package. Suitable for PCB mounting, breadboarding, and applications requiring higher power handling. Constructed with high-quality carbon film or metal film elements for stable performance. Lead-free and RoHS compliant construction."
        else:
            return f"Surface mount chip resistor with {resistance} resistance, {tolerance} tolerance, and {power} power rating in {package} package. Features {temp_coeff} temperature coefficient for stable performance across temperature range. Ideal for general purpose applications, signal processing, voltage division circuits, and current limiting. Manufactured using thick film technology on alumina ceramic substrate. RoHS compliant and suitable for lead-free soldering."
    
    elif 'CAP' in name_upper or 'CAPACITOR' in name_upper:
        capacitance = param_dict.get('Capacitance', '')
        voltage = param_dict.get('Voltage', '')
        tolerance = param_dict.get('Tolerance', '±10%')
        dielectric = param_dict.get('Dielectric', '')
        cap_type = param_dict.get('Type', '')
        
        if 'ALUM' in name_upper or 'ELECTROLYTIC' in name_upper or cap_type == 'Electrolytic':
            return f"Aluminum electrolytic capacitor with {capacitance} capacitance rated at {voltage} with {tolerance} tolerance. Radial leaded design in {package} package for through-hole mounting. Features low ESR and high ripple current capability. Ideal for power supply filtering, energy storage, and smoothing applications. Operating temperature range -40°C to +105°C. RoHS compliant."
        else:
            return f"Multilayer ceramic chip capacitor (MLCC) with {capacitance} capacitance rated at {voltage}. {dielectric} dielectric material provides excellent temperature stability and reliability. {package} SMD package for automatic pick-and-place assembly. Low ESL and ESR characteristics make it ideal for high-frequency decoupling, filtering, coupling, and bypassing applications. Suitable for power supplies, DC-DC converters, and digital circuits. Automotive grade available. RoHS compliant and halogen-free."
    
    elif 'INDUCTOR' in name_upper:
        inductance = param_dict.get('Inductance', '')
        tolerance = param_dict.get('Tolerance', '±20%')
        current = param_dict.get('Current', '')
        dcr = param_dict.get('DCR', '')
        
        if 'AXIAL' in name_upper:
            return f"Through-hole axial inductor with {inductance} inductance value and {tolerance} tolerance. Rated for {current} current handling capability. {package} package with axial leads for easy PCB mounting. Features low DCR for efficient power conversion. Suitable for power supplies, DC-DC converters, EMI filtering, and signal processing applications. Magnetically shielded construction minimizes electromagnetic interference. RoHS compliant."
        else:
            return f"Surface mount chip inductor with {inductance} inductance and {tolerance} tolerance in {package} package. Rated current: {current} with DCR of {dcr}. Compact size ideal for space-constrained applications. Suitable for DC-DC converters, power modules, RF circuits, filtering, and energy storage. Features high Q factor and excellent frequency characteristics. Ferrite core construction with wire-wound or multilayer design. RoHS compliant and suitable for automatic assembly."
    
    elif 'CRYSTAL' in name_upper:
        frequency = param_dict.get('Frequency', '')
        load_cap = param_dict.get('Load Capacitance', '')
        tolerance = param_dict.get('Tolerance', '±20ppm')
        temp_range = param_dict.get('Operating Temperature', '-20°C ~ 70°C')
        
        if 'THROUGH-HOLE' in name_upper:
            return f"Through-hole quartz crystal oscillator operating at {frequency} with {load_cap} load capacitance. ±{tolerance} frequency tolerance ensures accurate timing. Standard {package} metal can package with wire leads for easy PCB mounting. Temperature range: {temp_range}. Ideal for microcontrollers, embedded systems, real-time clocks, and communication devices requiring precise frequency reference. Low aging rate and excellent long-term stability. RoHS compliant."
        else:
            return f"Surface mount quartz crystal oscillator operating at {frequency} with {load_cap} load capacitance requirement. ±{tolerance} initial frequency tolerance with low aging characteristics. Compact {package} SMD package for space-efficient designs. Operating temperature: {temp_range}. Perfect for microcontrollers, FPGAs, CPUs, wireless modules, and timing circuits requiring stable frequency generation. Low power consumption and fast startup time. RoHS compliant and suitable for lead-free reflow soldering."
    
    elif 'MCU' in name_upper or 'MICROCONTROLLER' in name_upper:
        core = param_dict.get('Core', '')
        flash = param_dict.get('Flash', '')
        ram = param_dict.get('RAM', '')
        speed = param_dict.get('Speed', '')
        
        return f"Microcontroller unit based on {core} processor core with {flash} Flash memory and {ram} RAM. Operating at {speed} clock frequency. {package} package with multiple GPIO pins, peripherals including UART, SPI, I2C, ADC, timers, and PWM. Suitable for embedded systems, IoT devices, motor control, sensor interfacing, and industrial automation. Low power consumption with multiple sleep modes. Wide operating voltage range. Comprehensive development tools and software libraries available. RoHS compliant."
    
    elif 'OP-AMP' in name_upper or 'OPAMP' in name_upper or 'OPERATIONAL AMPLIFIER' in name_upper:
        opamp_type = param_dict.get('Type', 'Single')
        channels = param_dict.get('Channels', '1')
        bandwidth = param_dict.get('Bandwidth', '')
        
        return f"{opamp_type} operational amplifier with {channels} channel(s) in {package} package. Gain-bandwidth product: {bandwidth}. Features low offset voltage, low noise, and high slew rate. Rail-to-rail input/output capability for maximum signal swing. Ideal for signal conditioning, active filters, instrumentation amplifiers, comparators, and audio applications. Wide supply voltage range with low quiescent current. Industry-standard pinout. RoHS compliant."
    
    elif 'REGULATOR' in name_upper:
        reg_type = param_dict.get('Type', 'LDO')
        output_voltage = param_dict.get('Output Voltage', '')
        current = param_dict.get('Current', '')
        
        return f"{reg_type} voltage regulator providing {output_voltage} output at {current} maximum load current. {package} package with thermal shutdown and overcurrent protection. Features low dropout voltage, excellent line and load regulation, and low output noise. Built-in current limiting and thermal protection ensure safe operation. Ideal for powering microcontrollers, sensors, wireless modules, and other digital/analog circuits. Wide input voltage range with high PSRR. RoHS compliant."
    
    elif 'INTERFACE' in name_upper:
        ifc_type = param_dict.get('Type', '')
        channels = param_dict.get('Channels', '1')
        voltage = param_dict.get('Voltage', '')
        
        return f"{ifc_type} interface transceiver IC with {channels} channel(s) in {package} package. Operating voltage: {voltage}. Features ESD protection, low power consumption, and high data rate capability. Converts logic level signals for reliable communication over long distances or harsh environments. Includes transmitters and receivers with thermal shutdown protection. Suitable for industrial automation, PLCs, building control, and communication networks. Complies with relevant interface standards. RoHS compliant."
    
    elif 'TEMP' in name_upper or 'TEMPERATURE' in name_upper:
        sensor_type = param_dict.get('Type', 'Analog')
        temp_range = param_dict.get('Temperature Range', '-40°C ~ 125°C')
        accuracy = param_dict.get('Accuracy', '±1°C')
        
        return f"{sensor_type} temperature sensor with {accuracy} accuracy over {temp_range} range. {package} package suitable for SMD or through-hole mounting. Features low power consumption and fast response time. Output interface provides easy integration with microcontrollers and data acquisition systems. Ideal for thermal management, HVAC systems, medical devices, consumer electronics, and industrial temperature monitoring. Calibrated and tested at production. RoHS compliant."
    
    elif 'PRESSURE' in name_upper:
        press_range = param_dict.get('Range', '')
        output = param_dict.get('Output', 'Analog')
        
        return f"Pressure sensor with {press_range} measurement range and {output} output. {package} package with integrated signal conditioning. Features temperature compensation, high accuracy, and long-term stability. Measures absolute, gauge, or differential pressure depending on configuration. Ideal for HVAC systems, medical equipment, automotive applications, industrial process control, and environmental monitoring. Rugged construction with media compatibility. RoHS compliant."
    
    elif 'HUMIDITY' in name_upper:
        humid_type = param_dict.get('Type', 'Capacitive')
        accuracy = param_dict.get('Accuracy', '±3%')
        humid_range = param_dict.get('Range', '0-100%RH')
        
        return f"{humid_type} relative humidity sensor with {accuracy} accuracy over {humid_range}. {package} SMD package with digital or analog output. Features fast response time, low hysteresis, and excellent long-term stability. Integrated temperature sensor for dew point calculation. Suitable for weather stations, HVAC systems, industrial drying, agriculture, and consumer electronics. Factory calibrated with interchangeable without recalibration. RoHS compliant."
    
    elif 'MOTION' in name_upper or 'ACCELEROMETER' in name_upper or 'GYRO' in name_upper or 'IMU' in name_upper:
        motion_type = param_dict.get('Type', '')
        range_val = param_dict.get('Range', '')
        interface = param_dict.get('Interface', 'I2C/SPI')
        
        return f"{motion_type} sensor with {range_val} measurement range. {package} LGA package with {interface} digital interface. Features low noise, high resolution, and programmable bandwidth. Embedded FIFO buffer and interrupt generation for efficient data collection. Suitable for motion tracking, gesture recognition, image stabilization, navigation systems, gaming controllers, and wearable devices. Low power consumption with multiple operating modes. Factory calibrated. RoHS compliant."
    
    elif 'MAGNETIC' in name_upper or 'HALL' in name_upper:
        mag_type = param_dict.get('Type', 'Hall Effect')
        mode = param_dict.get('Mode', '')
        
        return f"{mag_type} sensor in {mode} configuration. {package} package with digital or analog output. Features high sensitivity, low offset, and temperature compensation. Suitable for position sensing, proximity detection, current sensing, rotary encoding, and magnetic field measurement. Applications include brushless motor commutation, speed detection, valve position sensing, and security systems. Wide operating temperature range. RoHS compliant."
    
    elif 'LIGHT' in name_upper:
        light_type = param_dict.get('Type', 'Ambient Light')
        interface = param_dict.get('Interface', 'Analog')
        
        return f"{light_type} sensor with {interface} output interface. {package} package with integrated photodiode and signal conditioning. Features wide dynamic range, human eye response matching, and IR rejection. Suitable for display backlight control, automatic brightness adjustment, proximity detection, and ambient light measurement. Applications include smartphones, tablets, laptops, automotive, and industrial equipment. Low power consumption. RoHS compliant."
    
    elif 'HEADER' in name_upper or 'CONNECTOR' in name_upper.split()[0] == 'HEADER':
        conn_type = param_dict.get('Type', 'Male')
        pins = param_dict.get('Pins', '')
        pitch = param_dict.get('Pitch', '')
        orientation = param_dict.get('Orientation', 'Straight')
        
        return f"{conn_type} pin header connector with {pins} positions at {pitch} pitch. {orientation} orientation in {package} mounting style. Features gold-plated contacts for reliable electrical connection and corrosion resistance. Suitable for board-to-board connections, ribbon cable termination, and general purpose interconnects. High current carrying capacity with low contact resistance. Standard pitch compatible with development boards and prototyping systems. UL94V-0 rated housing. RoHS compliant."
    
    elif 'USB' in name_upper:
        usb_type = param_dict.get('Type', 'USB')
        gender = param_dict.get('Gender', 'Receptacle')
        orientation = param_dict.get('Orientation', 'Right Angle')
        mounting = param_dict.get('Mounting', 'SMD')
        
        return f"{usb_type} connector {gender} in {orientation} configuration. {mounting} mounting style in {package} package. Features gold-plated contacts, EMI shielding, and robust mechanical design. Supports USB specifications for data transfer and power delivery. High insertion/extraction cycle life rating. Suitable for computers, peripherals, mobile devices, and embedded systems. Complies with USB interface standards. RoHS compliant and halogen-free."
    
    elif 'CARD' in name_upper:
        card_type = param_dict.get('Type', '')
        mechanism = param_dict.get('Mechanism', 'Push-Push')
        mounting = param_dict.get('Mounting', 'SMD')
        
        return f"{card_type} connector with {mechanism} mechanism in {mounting} mounting style. {package} package with spring-loaded contacts for reliable card retention and electrical connection. Features ESD protection, card detection switches, and write-protect sensing. Suitable for data storage applications, memory expansion, and removable media interfaces. High insertion cycle life with gold-plated contacts. Complies with card interface standards. RoHS compliant."
    
    elif 'TERMINAL' in name_upper or 'SCREW' in name_upper:
        wtb_type = param_dict.get('Type', 'Terminal Block')
        pins = param_dict.get('Pins', '')
        pitch = param_dict.get('Pitch', '')
        
        return f"{wtb_type} wire-to-board connector with {pins} positions at {pitch} pitch. {package} mounting style with screw or spring clamp termination. Features high current rating, wire gauge compatibility, and vibration-resistant connection. Suitable for power distribution, motor control, industrial automation, and field wiring applications. Accepts solid or stranded wires. Flame-retardant housing material. High voltage rating with creepage and clearance compliance. UL/CE certified. RoHS compliant."
    
    elif 'BOARD-TO-BOARD' in name_upper:
        pins = param_dict.get('Pins', '')
        pitch = param_dict.get('Pitch', '')
        height = param_dict.get('Height', '')
        
        return f"Board-to-board connector with {pins} positions at {pitch} pitch and {height} mated height. {package} SMD mounting with dual-row contact arrangement. Features self-alignment design, high retention force, and low insertion force. Gold-plated contacts ensure reliable signal integrity and current carrying capacity. Suitable for stacking applications, mezzanine connections, and modular system designs. High-speed signal transmission capable. Vibration and shock resistant. RoHS compliant."
    
    elif 'RF' in name_upper and 'CONNECTOR' in name_upper:
        rf_type = param_dict.get('Type', 'SMA')
        mounting = param_dict.get('Mounting', 'SMD')
        impedance = param_dict.get('Impedance', '50Ω')
        
        return f"{rf_type} RF coaxial connector in {mounting} mounting configuration. {package} package with {impedance} characteristic impedance. Features precision-machined contacts, PTFE/Teflon dielectric, and gold-plated center pin. Low VSWR and insertion loss for high-frequency applications. Suitable for RF and microwave systems, wireless communication, test equipment, and antenna connections. Frequency range from DC to several GHz. Durable mechanical design with multiple mating cycles. RoHS compliant."
    
    else:
        # Generic description
        return f"High-quality electronic component manufactured by {brand}. Model {model} in {package} package. Features reliable performance, consistent specifications, and excellent quality control. Suitable for various electronic applications including consumer electronics, industrial equipment, automotive systems, and telecommunications. Manufactured using advanced production processes with strict quality standards. RoHS compliant and environmentally friendly. Backed by manufacturer warranty and technical support."

def add_descriptions_to_file(input_file, output_file):
    """Add descriptions to all products in the JSON file."""
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Processing {len(products)} products...")
    count = 0
    for code, product in products.items():
        if 'productIntroEn' not in product or not product.get('productIntroEn'):
            product['productIntroEn'] = generate_description(product)
            count += 1
        
        if count % 1000 == 0 and count > 0:
            print(f"  Processed {count} products...")
    
    print(f"Added descriptions to {count} products")
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print("Done!")
    print(f"File size: {len(json.dumps(products, ensure_ascii=False)) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    add_descriptions_to_file('mock_products_large.json', 'mock_products_large.json')
