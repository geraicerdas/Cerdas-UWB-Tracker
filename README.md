# Repository Content
* **/Arduino Library** : Arduino library and example codes (.ino)
* **/GUI Visualization** : GUI Visualization of Anchor and Tags
* **/firmware** : Sample Arduino codes
* **/hardware** : Schematic (.pdf)
* **/images** : Images (.png)
* **/production** : gerber file for pcb manufacturing (.zip)

You can purchase this product from [![Generic badge](https://img.shields.io/badge/Indonesia-Tokopedia-<COLOR>.svg)](https://www.tokopedia.com/geraicerdas/cerdas-uwb-tracker-rtls-indoor-position-ultra-wideband-dw1000-dwm1000) 
[![Generic badge](https://img.shields.io/badge/Worldwide-Tindie-blue)](https://www.tindie.com/products/geraicerdas/cerdas-uwb-tracker/)

# Overview
### What is UWB?
Ultra-Wideband (UWB) is a radio technology that enables precise real-time location tracking and high-bandwidth communication over short distances. It uses low-power pulses across a wide spectrum, making it ideal for applications requiring accuracy (centimeter-level), security, and resistance to interference.

### Cerdas UWB Tracker
The Cerdas UWB Tracker is a versatile, open-source hardware platform built around the ESP32-S3 microcontroller. It supports two UWB modules (DWM1000 for 20-meter range and a long-range variant for 200 meters), enabling applications like asset tracking, indoor navigation, and IoT connectivity. With BLE, Wi-Fi, and expandable I/O, it’s designed for developers, makers, and researchers to build scalable location-aware systems.

[image here. to be updated]

# Key Features
### Hardware Features
- Core: ESP32-S3 with dual-core 240 MHz CPU, BLE 5.0, and Wi-Fi 4.
-  UWB Connectivity:
    - DWM1000 Version: ~20-meter range, ideal for prototyping and indoor use.
    - Long-Range Version: ~200-meter range for outdoor/industrial environments.
- Power Options:
  - USB-C for programming and power.
  - LiPo battery connector for portable use.
  - Slide switch for manual power control.
- Expandability:
  - 2x Qwiik connectors (Serial + I2C) for adding sensors, displays, or peripherals.
  - Optional unpopulated sensors:
    - BNO080 IMU: 9-axis motion tracking (accelerometer, gyroscope, magnetometer).
    - RV3028 RTC: Precision timekeeping with ultra-low power consumption.


# Technical Specifications
|Parameter | Details  |
| ------------- | :-----|
|MCU | ESP32-S3 (Wi-Fi 4, BLE 5.0, 512KB SRAM, 320KB ROM)|
|UWB Module	| DWM1000 (20m) or Long-Range Variant (200m)|
|Wireless	| Wi-Fi 4 (802.11 b/g/n), Bluetooth Low Energy 5.0|
|I/O Interfaces	| 2x Qwiik (Serial + I2C), USB-C|
|Power Input	| 5V via USB-C or 3.7V LiPo battery|
|Optional Sensors	| BNO080 (IMU), RV3028 (RTC) – unpopulated by default|
|PCB Size	| [To be updated]|

# Getting Started
### 1. Installation
- Install required libraries for DWM1000\
  Please only use this modified DW1000 library in this repo and put it in your Arduino IDE. This library support ESP32-S3 already
- Prepare your board in Programming mode\
  Press and hold IO0 button and then short press EN button, after that release IO0 button. Your computer will recognize the board, please check in Device Manager.
- Program the board via the USB-C port using Arduino IDE.\
  Please see the Arduino example code. Choose "ESP32S3 Dev Module" as your board
- At least you will need two Cerdas UWB Tracker for TWR application. Or at least four for RTLS

### 2. Basic Usage
- Power On: Use the slide switch to turn the board on.

### 3. Battery Tips
- Use a 3.7V LiPo battery (500–2000mAh recommended).
- Enable low-power modes in firmware to extend battery life.

# Advanced Usage
### Populating Optional Sensors
- BNO080: Solder the IMU for motion tracking (e.g., orientation data).
- RV3028: Add the RTC for timestamped data logging in low-power scenarios.

# Example Projects
- Indoor drone navigation using UWB anchors.
- Asset tracking in warehouses.
- Wearable motion tracker with BNO080 IMU sensor.
  
# Perform Anchor Calibration:
- Set up a tag using the ESP32_UWB_setup_tag.ino Arduino code. The antenna delay parameter should be set to the library default.
- Power up the tag and set it 7-8 m away from the anchor. Please take some measurement so it can more accurate.
- Edit ESP32_anchor_autocalibrate.ino and replace variable "this_anchor_target_dist" with your measured distance
```cpp
float this_anchor_target_distance = 7.19;
```
- Upload ESP32_UWB_anchor_autocalibrate.ino to your anchor device and open Serial Monitor
- Enter the reported anchor antenna delay to the ESP32_UWB_setup_anchor.ino code, specific for that anchor, and run that code to set up the anchor. Don't forget to set each anchor to have a unique anchor MAC address
```cpp
uint16_t Adelay = 16545;
```

# Development logs
V3.0
- Change to ESP32-S3 for compact, fast and powerfull applications
- Change resistors and capacitor size to the smaller package
- Added slide switch to turn on or off the board
- Added 2 Qwiik connectors (Serial and I2C) for futher development
- Added compatibility of original DWM1000, long range DWM1000 with Ceramic Antenna, and long range DWM1000 with SMA Antenna
- Change PCB finish to ENIG

V2.1
- Placed all parts in one side PCB
 
V1.3
- Added BNO080 High precision 9-DOF orientation IMU sensor manufactured by BOSCH

V1.2
- Added battery charging functionality, so you can use this module with LiPo battery powered.
- Change PCB color and fixing twisted silkscreen on pad 5V, 3.3V and GND

V1.0
- Initial design

# PCB and Parts [to be updated]
If you want to make the hardware yourself, just download the gerber file in production folder. Send it to your fav pcb manufacturer. And dont forget to get the Bill of materials :
|Qty | Part Name | Parts | MPN |
| ------------- |:-------------|:-------------| -----:|
| 6 | Capacitor 100nF 0603 | C3, C5, C8, C9, C10, C12 | |
| 7 | Resistor 10K 0603 | R1, R2, R7, R8, R15, R19, R20 | |
| 1 | Capacitor 10nF 0603 | C6 | |
| 5 | Capacitor 10uF 0603 | C1, C2, C4, C7, C11 | |
| 1 | Resonator 12Mhz 3213 | X1 | |
| 11 | Resistor 1K 0603 | R5, R6, R9, R10, R11, R12, R13, R14, R16, R17, R18 | |
| 1 | Diode 1N5819HW (SL) SOD-323 | D1 | |
| 2 | Resistor 4K7 0603 | R3, R4 | |
| 1 | Voltage Regulator AP2112K-3.3TRG1 SOT-23-5 | U1 | |
| 1 | LED BLUE 0805 | L4 | |
| 1 | Mosfet BSS138 SOT-23 | Q3 | |                                         
| 2 | Push Button YD3414 | S1, S2 | |
| 1 | CH340G SO-16 | U2 | | 
| 1 | DWM1000 Module | U4 | |
| 1 | ESP32-WROOM Module | U3 | |
| 1 | LED GREEN 0805 | L1 | |
| 6 | LED RED 0805 | L2, L3, L5, L6, L7, L8 | |
| 2 | Transistor S8050 SOT-23 | Q1, Q2 | |
| 1 | P-Mos SI2301 SOT-23 |Q4 | |
| 1 | USB Type C SMT 16P | J1 | |

Below is the previous version of Cerdas UWB Tracker. We keep this for your references.

Version 1.2
<p float="left">
<img src="https://images.tokopedia.net/img/cache/900/VqbcmM/2022/3/17/e9da7f10-681d-4bea-a63b-b9976f9db68b.jpg" width=280 /> 
<img src="https://images.tokopedia.net/img/cache/900/VqbcmM/2022/3/17/5a515c82-3fa7-4b73-b818-e37272c1a642.jpg" width=280 /> 
<img src="https://images.tokopedia.net/img/cache/900/VqbcmM/2022/3/17/9c192ba0-f1b4-4057-a05e-d9678923aef4.jpg" width=280 />
</p>

Version 1.0
<p float="left">
<img src="https://images.tokopedia.net/img/cache/900/VqbcmM/2021/12/24/b8c23ee2-33a5-4af8-ae1c-069759c55348.jpg" width=280 /> 
<img src="https://images.tokopedia.net/img/cache/900/VqbcmM/2021/12/24/65ec234b-f2c5-4a26-9dda-c24ea03e2e98.jpg" width=280 /> 
<img src="https://images.tokopedia.net/img/cache/900/VqbcmM/2021/12/24/12cd5dc7-a15d-48c4-a1e5-93ea75a33cd2.jpg" width=280 />
</p>

# Notice
In the first version, there are some twisted silkscreen as shown in the image below 

![image](images/Twisted%20Silkscreen%20Pins.png "Twisted Silkscreen")

5V should be GND <br>
GND (top) should be 5V <br>
3V3 should be GND <br>
GND (bottom) should be 3V3 <br>

# License
*We invests time and resources providing this open-source hardware, please support us by purchasing our products.*

*Designed by **[Insan Sains](https://www.youtube.com/insansains)** for **[Gerai Cerdas](https://geraicerdas.com)**, with contributions from the open source community. Creative Commons Attribution/Share-Alike, all text above must be included in any redistribution. See license.txt for additional information.*
