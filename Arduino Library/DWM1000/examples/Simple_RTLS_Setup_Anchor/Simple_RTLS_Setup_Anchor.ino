// UWB Anchor for Cerdas UWB Tracker V3.0
// by Gerai Cerdas
// based on DW1000Ranging_ANCHOR from arduino-DW1000 example library

/* Cerdas UWB Tracker V3.0 (will not work for previous version)

 * Please set :
 * USB CDC On Boot : "Enabled" 
 * USB DFU On Boot : "Disabled"
 * USB Firmware MSC On Boot : "Disabled"
 * Upload Mode : "UART0/Hardware CDC"
 * USB Mode : "USB-OTG (TinyUSB)"
 */


#include <SPI.h>
#include "DW1000Ranging.h"

#define EN_UWB 5

#define SPI_SCK 14
#define SPI_MISO 16
#define SPI_MOSI 18
#define DW_CS 33

// connection pins
const uint8_t PIN_RST = 7; // reset pin
const uint8_t PIN_IRQ = 13; // irq pin
const uint8_t PIN_SS = 33;   // spi select pin

// Do antenna delay calibration
//calibrated Antenna Delay setting for this anchor
uint16_t Adelay = 16580;

void setup() {
  // turn on UWB Module
  pinMode(EN_UWB, OUTPUT);
  digitalWrite(EN_UWB, HIGH);
  
  Serial.begin(115200);
  delay(1000);

  // init the configuration
  SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
  DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ);

  // set antenna delay for anchors only. Tag is default (16384)
  DW1000.setAntennaDelay(Adelay);
  
  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachBlinkDevice(newBlink);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);

  DW1000.enableDebounceClock();
  DW1000.enableLedBlinking();
  DW1000.setGPIOMode(MSGP0, LED_MODE);

  //we start the module as an anchor
  //DW1000Ranging.startAsAnchor("82:17:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_ACCURACY);
  //DW1000Ranging.startAsAnchor("82:17:5B:D5:A9:9A:E2:9C", DW1000.MODE_LONGDATA_RANGE_LOWPOWER);
  
  // Pilih salah satu untuk setiap Anchor
  // must disable randow short address, so we set to false
  DW1000Ranging.startAsAnchor("84:17:5B:D5:A9:9A:E2:9D", DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);
  //DW1000Ranging.startAsAnchor("83:17:5B:D5:A9:9A:E2:9D", DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);
  //DW1000Ranging.startAsAnchor("82:17:5B:D5:A9:9A:E2:9D", DW1000.MODE_LONGDATA_RANGE_LOWPOWER, false);

}

void loop() {
  DW1000Ranging.loop();
}

void newRange() {
  //    Serial.print("from: ");
  Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  Serial.print(", ");

#define NUMBER_OF_DISTANCES 1
  float dist = 0.0;
  for (int i = 0; i < NUMBER_OF_DISTANCES; i++) {
    dist += DW1000Ranging.getDistantDevice()->getRange();
  }
  dist = dist/NUMBER_OF_DISTANCES;
  Serial.println(dist);
}

void newBlink(DW1000Device* device) {
  Serial.print("blink; 1 device added ! -> ");
  Serial.print(" short:");
  Serial.println(device->getShortAddress(), HEX);
}

void inactiveDevice(DW1000Device* device) {
  Serial.print("delete inactive device: ");
  Serial.println(device->getShortAddress(), HEX);
}
