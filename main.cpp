/*
 * Swim Tracker Firmware
 * Hardware: ESP32 + ICM20948 (9-axis IMU)
 *
 * Reads accelerometer, gyroscope, and magnetometer data over I2C
 * and streams it to Serial at ~50Hz for Python visualization.
 *
 * Wiring:
 *   ICM20948 SDA --> GPIO 4
 *   ICM20948 SCL --> GPIO 5
 *   ICM20948 VCC --> 3.3V
 *   ICM20948 GND --> GND
 *   5.1kΩ pull-up resistors on SDA and SCL to 3.3V
 *
 * Serial output (space-separated, one line per sample):
 *   ax ay az gx gy gz mx my mz
 *   Units: m/s²  rad/s  µT
 *
 * IMPORTANT: Close Arduino Serial Monitor before running visualizer.py.
 * Both cannot hold the serial port at the same time.
 */

#include <Wire.h>
#include <Adafruit_ICM20948.h>
#include <Adafruit_Sensor.h>

Adafruit_ICM20948 icm;

void setup() {
  Serial.begin(115200);

  // Wait for USB serial to be ready (required for ESP32 USB CDC)
  while (!Serial) delay(10);
  delay(1000);

  Wire.begin(4, 5); // SDA=GPIO4, SCL=GPIO5

  if (!icm.begin_I2C(0x68)) {
    Serial.println("ICM20948 not found - check wiring and I2C address");
    while (1) {
      delay(1000);
      Serial.println("Retrying...");
    }
  }

  icm.setAccelRange(ICM20948_ACCEL_RANGE_4_G);    // ±4G
  icm.setGyroRange(ICM20948_GYRO_RANGE_500_DPS);  // ±500 deg/s

  // The magnetometer (AK09916) is a separate chip inside the ICM20948.
  // It needs extra time to wake up after the main chip initializes.
  delay(500);

  // Python skips lines starting with letters, so this header is safe to send
  Serial.println("ax ay az gx gy gz mx my mz");
}

void loop() {
  sensors_event_t accel, gyro, mag, temp;
  icm.getEvent(&accel, &gyro, &temp, &mag);

  Serial.print(accel.acceleration.x); Serial.print(" ");
  Serial.print(accel.acceleration.y); Serial.print(" ");
  Serial.print(accel.acceleration.z); Serial.print(" ");
  Serial.print(gyro.gyro.x);          Serial.print(" ");
  Serial.print(gyro.gyro.y);          Serial.print(" ");
  Serial.print(gyro.gyro.z);          Serial.print(" ");
  Serial.print(mag.magnetic.x);       Serial.print(" ");
  Serial.print(mag.magnetic.y);       Serial.print(" ");
  Serial.println(mag.magnetic.z);

  // 50Hz sample rate
  // 100Hz caused serial buffer buildup — Python couldn't keep up at that rate
  delay(20);
}
