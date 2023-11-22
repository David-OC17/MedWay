#include <Arduino.h>
#include <DHT.h>
#include <TinyGPS++.h>
#include "MPU6050_6Axis_MotionApps20.h"


// MACROS
#define DHT_PIN 4
#define DHTTYPE DHT22
#define MPU_INTERRUPT_PIN 27

// Constants
const int time2send = 3000;
const int time2sample_dht = 1000;

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
float real_ypr[3];

// Time management
unsigned long time_aux = 0;

///// MPU INTERRUPT /////////////////////////
volatile bool mpu_interrupt = false;
void dmpDataReady(){
  mpu_interrupt = true;
}
/////////////////////////////////////////////

void setup() {
  // UART channels
  Serial.begin(115200);
  Serial2.begin(9600);

  // I2C communication
  Wire.begin();

  // DHT temperature sensor
  dht.begin();

  // MPU and DMP init
  Serial.println(mpu.testConnection()? "MPU connected succesfully" : "MPU failed to connect");
  device_status = mpu.dmpInitialize();

  // MPU DMP status handling
  if(device_status == 0){
    mpu.setDMPEnabled(true);

    // Calibrate 
    mpu.CalibrateAccel(7);
    mpu.CalibrateGyro(7);

    // Config interrupt
    attachInterrupt(digitalPinToInterrupt(MPU_INTERRUPT_PIN), dmpDataReady, RISING);
    interrupt_status = mpu.getIntStatus();

    // Update dmp ready flag to true
    Serial.println("\nMPU DMP is ready to use");
    dmp_ready = true;
    
    packet_size = mpu.dmpGetFIFOPacketSize();  // Expected packet size for dmp

  }else{
    // Error: 1 = Initial memory load failed, 2 = DMP configuration updates failed
    Serial.println("DMP config failed with code " + String(device_status));
  }
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
      char c = Serial2.read();
      if (gps.encode(c)){   // If a valid sentence comes in get data
        lat = gps.location.lat();
        lon = gps.location.lng();
        meters = gps.altitude.meters();
        sats = gps.satellites.value();
      }
    }
    time_aux = millis();
  }

  // If dmp was configured succesfully read available packet to fifo buffer
  if(dmp_ready){
    if(mpu.dmpGetCurrentFIFOPacket(fifoBuffer)){
      // Get yaw/pitch/roll in array
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      mpu.dmpGetGravity(&gravity, &q);
      mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

      // Get acceleration
      mpu.dmpGetAccel(&aa, fifoBuffer);
      mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);
      Serial.print("areal\t");
      Serial.print(aaReal.x);
      Serial.print("\t");
      Serial.print(aaReal.y);
      Serial.print("\t");
      Serial.println(aaReal.z);

      // Serial.print("ypr\t");
      // Serial.print(ypr[0] * 180/M_PI);
      // Serial.print("\t");
      // Serial.print(ypr[1] * 180/M_PI);
      // Serial.print("\t");
      // Serial.println(ypr[2] * 180/M_PI);
    }
  }

  delay(100);
}