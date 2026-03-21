/**
 * swim-tracker / main.cpp
 *
 * Initial IMU communication over I2C using the ICM-20948.
 * Status: Partial — communication established but unstable (crashes after short runtime).
 *
 * Board:  ESP32
 * IDE:    Arduino IDE
 *
 * ESP32 default I2C pins:
 *   SDA → GPIO 21
 *   SCL → GPIO 22
 *
 * Author: Jun (@ijun30225)
 */

#include <Adafruit_I2CDevice.h>

#define I2C_ADDRESS 0x68  // ICM-20948 default I2C address (AD0 low)

Adafruit_I2CDevice i2c_dev = Adafruit_I2CDevice(I2C_ADDRESS);

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  Serial.println("Swim Tracker — IMU Init");

  if (!i2c_dev.begin()) {
    Serial.println("ERROR: Could not find IMU at address 0x68. Check wiring.");
    while (1);
  }

  Serial.println("IMU found! Beginning communication...");
}

void loop() {
  // TODO: Read accelerometer and gyroscope registers
  // TODO: Parse raw data into usable values
  // TODO: Detect strokes, laps, and turns

  delay(100);
}
