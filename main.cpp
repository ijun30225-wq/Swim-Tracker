#include <Wire.h>
#include <Adafruit_ICM20948.h>
#include <Adafruit_Sensor.h>

Adafruit_ICM20948 icm;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(4, 5); // SDA=4, SCL=5

  if (!icm.begin_I2C(0x68)) {
    Serial.println("Failed to find ICM20948");
    while (1);
  }

  Serial.println("ICM20948 ready");
  Serial.println("ax,ay,az,gx,gy,gz");
}

void loop() {
  sensors_event_t accel, gyro, temp;
  icm.getEvent(&accel, &gyro, &temp);

  // Acceleration in m/s^2
  Serial.print(accel.acceleration.x); Serial.print(",");
  Serial.print(accel.acceleration.y); Serial.print(",");
  Serial.print(accel.acceleration.z); Serial.print(",");

  // Gyro in rad/s
  Serial.print(gyro.gyro.x); Serial.print(",");
  Serial.print(gyro.gyro.y); Serial.print(",");
  Serial.println(gyro.gyro.z);

  delay(25);
}
