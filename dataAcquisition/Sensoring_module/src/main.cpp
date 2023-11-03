#include <Arduino.h>
#include <DHT.h>
#include <TinyGPS++.h>

// MACROS
#define DHT_PIN 4
#define DHTTYPE DHT22

// Constants
const int time2send = 3000;
const int time2sample_dht = 1000;

// Sensores
DHT dht(DHT_PIN, DHTTYPE, 22);
TinyGPSPlus gps;

// Global vars
float hum, temp;
unsigned int meters = 0;
uint8_t sats = 0;

// Time management
unsigned long time_aux = 0;

void setup() {
  Serial.begin(9600);
  Serial2.begin(4800, SERIAL_8N1, 16, 17);  
  dht.begin();
}

void loop() {
  if(millis() - time_aux >= time2send){
    // GPS
    if(Serial2.available()){
      sats = gps.satellites.value();
      meters = gps.altitude.meters();
      Serial.println("Temperatura: " + String(temp));
      Serial.println("Humedad: " + String(hum));
      Serial.println("Satelites " + String(sats));
      Serial.println("Altura: " + String(meters) + "\n");
    }

    // DHT section
    hum = dht.readHumidity();
    temp = dht.readTemperature();

    // Print
    time_aux = millis();
  }
  delay(10);
}