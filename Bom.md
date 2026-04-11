# Bill of Materials

Components used in the current prototype.

| Component | Part | Notes |
|-----------|------|-------|
| Microcontroller | ESP32 Dev Module | USB-C variant preferred |
| IMU | ICM-20948 breakout | 9-axis: accel + gyro + mag |
| Resistors | 5.1kΩ x2 | Pull-ups on SDA and SCL to 3.3V |
| Breadboard | Full-size | For prototyping only — not for water use |
| Jumper wires | M-M | Enough for I2C (4 wires) |
| USB cable | USB-A to USB-C | For flashing and serial data |

---

## Notes

- The ICM-20948 breakout board requires header pins to be soldered before use.
- Breadboard connections are not reliable for any physical activity — solder before testing on the body.
- The ESP32's 3.3V pin supplies the ICM20948. Do not use 5V — it will damage the sensor.
- Pull-up resistors are required for I2C stability. Without them, the bus floats and behavior is unpredictable.

---

## Future / Planned Components

| Component | Purpose |
|-----------|---------|
| LiPo battery + charger | Wireless operation |
| Waterproof enclosure | In-water use |
| Custom PCB | Replace breadboard, reduce size |
| BLE module (built into ESP32) | Wireless data streaming |
