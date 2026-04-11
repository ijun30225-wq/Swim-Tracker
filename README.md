# Swim Tracker

A wearable swim tracking system built from scratch — collecting real-time motion data from an IMU sensor to eventually analyze swim performance.

Personal engineering project. ECE student learning embedded systems, sensor interfacing, and signal processing by building something real.

---

## Project Goals

- Build a waterproof wearable for swimmers
- Track motion with a 9-axis IMU (accelerometer + gyroscope + magnetometer)
- Visualize and log sensor data in real time
- Extract swim metrics: stroke count, lap detection, efficiency scoring

---

## Status

| Area | Status |
|---|---|
| I2C IMU communication | Working |
| Stable sensor readings | Working |
| Python live visualization | Working |
| CSV data logging | Working |
| Sensor fusion (orientation) | Not started |
| 3D browser visualization | Not started |
| Motion / stroke analysis | Not started |
| Waterproof enclosure | Not started |

---

## Hardware

| Component | Detail |
|---|---|
| Microcontroller | ESP32 Dev Module |
| IMU | ICM-20948 (accel + gyro + magnetometer, 9-axis) |
| Interface | I2C |
| I2C Address | `0x68` |
| Pull-up resistors | 5.1kΩ on SDA and SCL to 3.3V |

See [`Bom.md`](Bom.md) for the full parts list.

### Wiring

| ESP32 Pin | ICM-20948 Pin |
|---|---|
| GPIO 4 | SDA |
| GPIO 5 | SCL |
| 3.3V | VCC |
| GND | GND |

---

## Software

### Dependencies

- [`Adafruit ICM20948`](https://github.com/adafruit/Adafruit_ICM20X) — IMU driver
- [`Adafruit BusIO`](https://github.com/adafruit/Adafruit_BusIO) — I2C abstraction layer

Install both via **Arduino IDE → Tools → Manage Libraries**.

Python dependencies:

```bash
pip install pyserial matplotlib pandas
```

### Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/ijun30225/swim-tracker.git
   cd swim-tracker
   ```

2. Open `main.cpp` in Arduino IDE

3. Install the two Arduino libraries above via Library Manager

4. Select board: **ESP32 Dev Module** (Tools → Board → ESP32 Arduino)

5. Select your COM port and click Upload

6. To view raw data: open Serial Monitor at `115200` baud

7. To run the Python visualizer, **close Serial Monitor first**, then:
   ```bash
   cd src
   python visualizer.py
   ```
   Update the `PORT` variable in `visualizer.py` to match your system.

---

## How It Works

The ESP32 reads all 9 sensor axes from the ICM20948 over I2C and streams them as space-separated values over USB serial at 50Hz:

```
ax ay az gx gy gz mx my mz
```

The Python visualizer reads that stream, plots it live in a rolling window, and saves everything to a CSV on close. See [`Debugging.md`](Debugging.md) for issues encountered and how they were resolved.

---

## Roadmap

**Short term**
- [x] I2C communication with ICM20948
- [x] Stable 50Hz data stream
- [x] Live Python visualization
- [x] CSV data logging
- [ ] Solder connections for physical reliability

**Medium term**
- [ ] Sensor fusion filter (Madgwick/Mahony) to compute orientation
- [ ] 3D browser visualization (Flask + WebSocket + Three.js)
- [ ] Basic stroke detection from motion patterns

**Long term**
- [ ] Lap counting and performance metrics
- [ ] Wireless streaming over BLE
- [ ] Compact waterproof enclosure
- [ ] Mobile app

---

## Repo Structure

```
swim-tracker/
├── src/
│   └── visualizer.py     # Real-time Python visualizer + CSV logger
├── main.cpp              # ESP32 firmware (Arduino IDE)
├── Bom.md                # Bill of materials
├── Debugging.md          # Running log of issues and fixes
├── .gitignore
└── README.md
```

---

## Author

**Jun Iguchi** — Electrical & Computer Systems Engineering, RPI  
GitHub: [@ijun30225](https://github.com/ijun30225)
