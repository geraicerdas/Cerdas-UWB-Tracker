# UWB Positioning System Simulator

A Python-based GUI system for simulating Ultra-Wideband (UWB) tag positioning using 2-anchor and 3-anchor configurations.

![UWB Two Anchor Visualization](https://github.com/user-attachments/assets/fa5eac44-512b-4149-a3b9-6882c797655f)
![UWB Three Anchor Visualization](https://github.com/user-attachments/assets/386eb665-07bf-41d6-8d48-333e2b5612a0)

## Features
- 📡 Real-time visualization of UWB tag position
- ⚙️ Supports both 2-anchor and 3-anchor configurations
- 📶 Simulates distance measurements between anchors and tags
- 🌐 Network-based communication model

## Hardware Requirements
- 2 Cerdas UWB Tracker for 2-anchor visualization, or 3 Cerdas UWB Tracker for 3-anchor visualization
- 1 Cerdas UWB Tracker as a Tag
- Arduino IDE for firmware upload
- Python 3.8+ environment

## Setup Guide

### 1. Anchor Setup
Using code `Simple_RTLS_Setup_Anchor.ino`  
**Important**: Use unique addresses for each anchor:
- 3-anchor setup: Use addresses 84, 83, and 82
- 2-anchor setup: Use addresses 83 and 82
```arduino
  // Pilih salah satu untuk setiap Anchor
  // must disable randow short address, so we set to false
  DW1000Ranging.startAsAnchor("84:17:5B:D5:A9:9A:E2:9D", DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);
  //DW1000Ranging.startAsAnchor("83:17:5B:D5:A9:9A:E2:9D", DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);
  //DW1000Ranging.startAsAnchor("82:17:5B:D5:A9:9A:E2:9D", DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);

// Keep other parameters default
```

### 2. Tag Setup
Using code Simple_RTLS_Setup_Tag.ino\
Please configure your network credentials
```arduino
const char *ssid = "******"; // fill with your SSID name
const char *password = "********";  // fill with the wifi password
const char *host = "192.168.1.6"; // fill with your python server IP address
```
### 3. Running the Python Code
Install the dependencies\
pip install numpy pygame

### 4. Usage Instructions
1. Position anchors 3 meters apart in either:
   - Linear configuration for 2-anchor setup
   - Triangular configuration for 3-anchor setup
4. Power on all anchors and tag devices
5. Start the Python visualization server
