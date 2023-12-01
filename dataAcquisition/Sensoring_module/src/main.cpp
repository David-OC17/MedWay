#include <Arduino.h>
#include <DHT.h>
#include <TinyGPS++.h>
#include "MPU6050_6Axis_MotionApps20.h"
#include "WiFi.h"

// MACROS
#define DHT_PIN 4
#define DHTTYPE DHT22
#define MPU_INTERRUPT_PIN 27
#define EN_LED 0
#define RED 27
#define GREEN 14
#define BLUE 12
#define BUZZER 13
 
// Constants
const int time2send = 3000;
const int time2sample_dht = 1000;

// Flags
bool wifi_connected = false;
bool mpu_connected = false;

// Sensores
DHT dht(DHT_PIN, DHTTYPE, 22);
TinyGPSPlus gps;
MPU6050 mpu;

// GLOBAL VARS FOR TELEMETRY //
// DHT vars
float hum, temp;

// GPS vars
float lat, lon;
float meters = 0;
uint8_t sats = 0;

// MPU Control vars
bool dmp_ready = false;
uint8_t device_status;
uint8_t interrupt_status;
uint8_t fifoBuffer[64];
uint16_t packet_size;
uint16_t fifo_count;

// DMP Vars
Quaternion q;
VectorInt16 aa;     // Raw acceleration from the sensor
VectorInt16 aaReal;
VectorFloat gravity;
float ypr[3];       // Yaw, Pitch, Roll
float average_array[50];
float mean_accel;
uint8_t accel_count;

// Time management
unsigned long time_aux = 0;

// Send data
String data = "";

///// MPU INTERRUPT /////////////////////////
volatile bool mpu_interrupt = false;
void dmpDataReady(){
  mpu_interrupt = true;
}
/////////////////////////////////////////////

void getGpsInfo(){
  char c = Serial2.read();
      if (gps.encode(c)){   // If a valid sentence comes in get data
        lat = gps.location.lat();
        lon = gps.location.lng();
        meters = gps.altitude.meters();
        sats = gps.satellites.value();
      }
}

void getMpuData(){
  // If dmp was configured succesfully read available packet to fifo buffer
  if(mpu.dmpGetCurrentFIFOPacket(fifoBuffer)){
      // Get yaw/pitch/roll in array
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      mpu.dmpGetGravity(&gravity, &q);
      mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

      // Get acceleration
      mpu.dmpGetAccel(&aa, fifoBuffer);
      mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);   // For our needs aaReal is better because it depreciates the constant effect of gravity
      
      // Average
      mean_accel = (aaReal.x + aaReal.y + aaReal.z) / 3;
  }
}

void updateRGBStat(){
  if(wifi_connected && mpu_connected){
    Serial.println("All working fine");
    analogWrite(RED, 0);     // GREEN (working fine)
    analogWrite(GREEN, 255);
    analogWrite(BLUE, 0);
  }else if(wifi_connected && !mpu_connected){
    analogWrite(RED, 255);     // PURPLE
    analogWrite(GREEN, 0);
    analogWrite(BLUE, 255);
  }else if(!wifi_connected && mpu_connected){
    analogWrite(RED, 0);     // ORANGE
    analogWrite(GREEN, 255);
    analogWrite(BLUE, 0);
  }else{
    analogWrite(RED, 255);   // RED (nothing works)
    analogWrite(GREEN, 0);
    analogWrite(BLUE, 0);
  }
}

//////////////////////////////////////////

void setup() {
  // UART channels
  Serial.begin(115200);
  Serial2.begin(9600);

  // I2C communication
  Wire.begin();

  // DHT temperature sensor
  dht.begin();

  // Enable LEDS
  pinMode(BUZZER, OUTPUT);
  pinMode(EN_LED, OUTPUT);
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);

  // MPU and DMP init
  Serial.println(mpu.testConnection()? "MPU connected succesfully" : "MPU failed to connect");
  device_status = mpu.dmpInitialize();

  // Blue while calibrating
  analogWrite(BLUE, 255);
  analogWrite(RED, 0);
  analogWrite(GREEN, 0);

  // MPU DMP status handling
  if(device_status == 0){
    mpu_connected = true;
    mpu.setDMPEnabled(true);

    // Calibrate 
    mpu.CalibrateAccel(7);
    mpu.CalibrateGyro(7);

    // Config interrupt
    attachInterrupt(digitalPinToInterrupt(MPU_INTERRUPT_PIN), dmpDataReady, RISING);
    interrupt_status = mpu.getIntStatus();

    // Update dmp ready flag to true
    Serial.println("\nMPU DMP is ready to use");
    // dmp_ready = true;
    
    packet_size = mpu.dmpGetFIFOPacketSize();  // Expected packet size for dmp
  }else{
    // Error: 1 = Initial memory load failed, 2 = DMP configuration updates failed
    Serial.println("DMP config failed with code " + String(device_status));
    mpu_connected = false;
  }
  
  // Update RGB LED as flag
  updateRGBStat();

  // Start sound !
  while(millis() < 2500){
    digitalWrite(BUZZER, HIGH);
  }
  
  digitalWrite(BUZZER, LOW);
}

/////////////////////////////////////////////

void loop() {
  // While there is no available data from MPU
  if(millis() - time_aux >= time2send){
    // DHT section
    hum = dht.readHumidity();
    temp = dht.readTemperature();

    // GPS Section
    while (Serial2.available())
    {
      // Get currently available info in serial2 from gps
      getGpsInfo();
    }

    // PRINT DATA
    Serial.println("Temperature: " + String(temp));
    Serial.println("Humidity: " + String(hum));
    Serial.println("Longitude: " + String(lon));
    Serial.println("Latitude: " + String(lat));
    Serial.println("Altitude: " + String(meters));
    Serial.println("Acceleration: " + String(aaReal.x) + " " + String(aaReal.y) + " " + String(aaReal.z));
    Serial.println("Gyroscope: " + String(ypr[0] * 180/M_PI) + " " + String(ypr[1] * 180/M_PI) + " " + String(ypr[2] * 180/M_PI) + "\n");

    data = String(temp) + "," + String(hum) + "," + String(lon) + "," + String(lat) + "," + String(meters) + "," + 
           String(aaReal.x) + "," + String(aaReal.y) + "," + String(aaReal.z) + "," + String(ypr[0] * 180/M_PI) + "," 
           + String(ypr[1] * 180/M_PI) + "," + String(ypr[2] * 180/M_PI);

    Serial.println(data);

    time_aux = millis();
  }

  // Get MPU data
  if(mpu_connected){
    getMpuData();
  }

  delay(100);
}