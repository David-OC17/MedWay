#include <Arduino.h>
#include <DHT.h>
#include <TinyGPS++.h>

// MACROS
#define DHT_PIN 4
#define DHTTYPE DHT22

// Constants
const int time2send = 3000;
const int time2sample_dht = 1000;

// Communication
// EspSoftwareSerial::UART ss_gps;

// Sensores
DHT dht(DHT_PIN, DHTTYPE, 22);
TinyGPSPlus gps;

// GLOBAL VARS FOR TELEMETRY //
// DHT vars
float hum, temp;
// GPS vars
float lat, lon;
float meters = 0;
uint8_t sats = 0;

// Time management
unsigned long time_aux = 0;

void setup() {
  // UART channels
  Serial.begin(9600);
  Serial2.begin(9600);

  // DHT temperature sensor
  dht.begin();
}

void loop() {
  if(millis() - time_aux >= time2send){

    // DHT section
    hum = dht.readHumidity();
    temp = dht.readTemperature();

    // GPS Section
    while (Serial2.available())
    {
      char c = Serial2.read();
      if (gps.encode(c)){   // If a valid sentence comes in get data
        lat = gps.location.lat();
        lon = gps.location.lng();
        meters = gps.altitude.meters();
        sats = gps.satellites.value();
      }
    }

    // Print data
    Serial.println("Temperatura: " + String(temp));
    Serial.println("Humedad: " + String(hum));
    Serial.println("Longitud: " + String(lon));
    Serial.println("Latitud: " + String(lat));
    Serial.println("Satelites " + String(sats));
    Serial.println("Altura: " + String(meters) + "\n");

    time_aux = millis();
  }
  delay(10);
}