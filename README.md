### Repository Content
* **/firmware** : Arduino example codes (.ino)
* **/hardware** : Schematic (.pdf)
* **/production** : gerber file for pcb manufacturing (.zip)

You can purchase this product from [![Generic badge](https://img.shields.io/badge/Indonesia-Tokopedia-<COLOR>.svg)](https://www.tokopedia.com/geraicerdas/cerdas-uwb-tracker-rtls-indoor-position-ultra-wideband-dw1000-dwm1000) 
[![Generic badge](https://img.shields.io/badge/Worldwide-Unavailable-red.svg)](https://geraicerdas.com)

# Cerdas UWB Tracker
This is UWB DWM1000 Development Board with ESP32 as a main controller. It also compatible with BU01, the UWB module DW1000 from Ai-Thinker. As you know Ultra-Wide Band is a radio technology that can use a very low energy level for short-range, high-bandwidth communications over a large portion of the radio spectrum. Most recent applications target sensor data collection, precision locating and tracking applications. Some of high-end smartphones has used with this technology.

MCU + Wifi + Bluetooth + UWB in one devices. 
There are some additional features that has not been tested yet : 
- 3xAA battery connector
- SMT stackable header 2x13P

## How To Use
At least you will need two Cerdas UWB Tracker.
In the Arduino IDE, make sure :
- you have installed ESP32 in the board manager
- install library : [arduino-dw1000](https://github.com/thotro/arduino-dw1000) by Thotro
- Edit code in DW1000.cpp

find this line 165

```cpp
void DW1000Class::begin(uint8_t irq, uint8_t rst) {
```

You will see this block line (173-175)
```cpp
 #ifndef ESP8266
 	SPI.usingInterrupt(digitalPinToInterrupt(irq)); // not every board support this, e.g. ESP8266
 #endif
```

disable that block line, so the result will be like this :
```cpp
// #ifndef ESP8266
// 	SPI.usingInterrupt(digitalPinToInterrupt(irq)); // not every board support this, e.g. ESP8266
// #endif
```
- Now you can try an example sketches in this repo. Don't forget to select "ESP32 Dev Board" when uploading

## PCB and Parts
If you want to make your self, just download the gerber file in production folder. Send it to your fav pcb manufacturer. And dont forget to get the Bill of materials :
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

<p float="left">
<img src="https://images.tokopedia.net/img/cache/900/VqbcmM/2021/12/24/b8c23ee2-33a5-4af8-ae1c-069759c55348.jpg" width=400 /> 
<img src="https://images.tokopedia.net/img/cache/900/VqbcmM/2021/12/24/65ec234b-f2c5-4a26-9dda-c24ea03e2e98.jpg" width=400 /> 
<img src="https://images.tokopedia.net/img/cache/900/VqbcmM/2021/12/24/12cd5dc7-a15d-48c4-a1e5-93ea75a33cd2.jpg" width=805 />
</p>

## License
*We invests time and resources providing this open-source hardware, please support us by purchasing our products.*

*Designed by **[Insan Sains](https://www.youtube.com/insansains)** for **[Gerai Cerdas](https://geraicerdas.com)**, with contributions from the open source community. Creative Commons Attribution/Share-Alike, all text above must be included in any redistribution. See license.txt for additional information.*
