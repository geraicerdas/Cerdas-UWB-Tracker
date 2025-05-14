// UWB Tag for Cerdas UWB Tracker V3.0
// by Gerai Cerdas
// based on DW1000Ranging_TAGS from arduino-DW1000 example library

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
#include <WiFi.h>
#include "link.h"

#define EN_UWB 5

#define SPI_SCK 14
#define SPI_MISO 16
#define SPI_MOSI 18
#define DW_CS 33

// connection pins
const uint8_t PIN_RST = 7; // reset pin
const uint8_t PIN_IRQ = 13; // irq pin
const uint8_t PIN_SS = 33;   // spi select pin

// calibration range
// for this time, we used hard-coded based on actual measurement
// TODO : 
// Do antenna delay calibration
//float calibrationRange = 0.78;
//float calibrationRange = 1.00;

const char *ssid = "******"; // fill with your SSID name
const char *password = "********";  // fill with the wifi password
const char *host = "192.168.1.6"; // fill with your python server IP address
WiFiClient client;

struct MyLink *uwb_data;
int index_num = 0;
long runtime = 0;
String all_json = "";

void setup() {
  // turn on UWB Module
  pinMode(EN_UWB, OUTPUT);
  digitalWrite(EN_UWB, HIGH);
  
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected");
  Serial.print("IP Address:");
  Serial.println(WiFi.localIP());

  if (client.connect(host, 80)) {
    Serial.println("Success");
    //client.print(String("GET /") + " HTTP/1.1\r\n" +
    //             "Host: " + host + "\r\n" +
    //             "Connection: close\r\n" +
    //             "\r\n");
  } else {
    Serial.println("not connected to UDP server");
  }

  delay(1000);

  // init the configuration
  SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
  DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ); //Reset, CS, IRQ pin
  
  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachNewDevice(newDevice);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);
  //Enable the filter to smooth the distance
  //DW1000Ranging.useRangeFilter(true);

  DW1000.enableDebounceClock();
  DW1000.enableLedBlinking();
  DW1000.setGPIOMode(MSGP0, LED_MODE);

  //we start the module as a tag
  //DW1000Ranging.startAsTag("7D:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_LOWPOWER);
  DW1000Ranging.startAsTag("6D:00:22:EA:82:60:3B:9C", DW1000.MODE_LONGDATA_RANGE_LOWPOWER);

  uwb_data = init_link();
  runtime = millis();
}

void loop() {
  DW1000Ranging.loop();
  if ((millis() - runtime) > 100) {
    //Serial.println("ini dijalankan");
    make_link_json(uwb_data, &all_json);
    //Serial.println("make json link completed");
    send_udp(&all_json);
    runtime = millis();
  }
}

void newRange() {
  char c[30];
  //Serial.print("from: "); Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
  ////Serial.print("\t Range: "); Serial.print(DW1000Ranging.getDistantDevice()->getRange()); Serial.print(" m");
  //Serial.print("\t Range: "); Serial.print(DW1000Ranging.getDistantDevice()->getRange() * calibrationRange ); Serial.print(" m");
  //Serial.print("\t RX power: "); Serial.print(DW1000Ranging.getDistantDevice()->getRXPower()); Serial.println(" dBm");
  fresh_link(uwb_data, DW1000Ranging.getDistantDevice()->getShortAddress(), DW1000Ranging.getDistantDevice()->getRange(), DW1000Ranging.getDistantDevice()->getRXPower());
}

void newDevice(DW1000Device *device) {
  Serial.print("ranging init; 1 device added ! -> ");
  Serial.print(" short:");
  Serial.println(device->getShortAddress(), HEX);
  add_link(uwb_data, device->getShortAddress());
}

void inactiveDevice(DW1000Device *device) {
  Serial.print("delete inactive device: ");
  Serial.println(device->getShortAddress(), HEX);
  delete_link(uwb_data, device->getShortAddress());
}

void send_udp(String *msg_json) {
  if (client.connected()) {
    //Serial.println("mau kirim UDP");
    client.print(*msg_json);
    //delay(100);
    //Serial.println("UDP sent");
  }
}


