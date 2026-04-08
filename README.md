# 🏊 Swim Tracker

A wearable swim tracking system built from scratch — collecting real-time motion and orientation data to analyze swim performance.

> Personal engineering project by Jun — ECE student learning embedded systems, sensor interfacing, and signal processing through building.

---

## Project Goals

- Build a **waterproof wearable device** for swimmers
- Track motion using an **IMU sensor** (accelerometer + gyroscope)
- Process and interpret swim data
- Extract meaningful metrics: stroke count, lap detection, and efficiency scores

---

## Status

| Area | Status |
|---|---|
| I2C IMU Communication | ✅ Working |
| Stable Sensor Readings | ✅ Working |
| Python Visualization | 🟡 In Progress |
| Data Logging | 🔴 Not Started |
| Motion Analysis | 🔴 Not Started |
| Waterproof Enclosure | 🔴 Not Started |

---

## Hardware

| Component | Details |
|---|---|
| IMU Sensor | ICM-20948 (6-axis accel + gyro) |
| Microcontroller | ESP32 |
| Communication | I2C |
| I2C Address | `0x68` (default) |
| IDE | Arduino IDE |

### Wiring

| ESP32 Pin | ICM-20948 Pin |
|---|---|
| GPIO 4 | SDA |
| GPIO 5 | SCL |
| 3.3V | VCC |
| GND | GND |

Note: 5.1kΩ pull-up resistors on SDA and SCL to 3.3V. Header pins must be soldered to breakout board.

---

## Software

### Dependencies

- [`Adafruit_BusIO`](https://github.com/adafruit/Adafruit_BusIO) — for `Adafruit_I2CDevice`

Install via **Arduino IDE → Tools → Manage Libraries → search "Adafruit BusIO"**.

### Getting Started

1. Clone this repo:
   ```bash
   git clone https://github.com/ijun30225/swim-tracker.git
   cd swim-tracker
   ```

2. Open `src/main.cpp` in Arduino IDE

3. Install the `Adafruit BusIO` library via Library Manager

4. Select board: **ESP32 Dev Module** (or your specific ESP32 variant)  
   *(Tools → Board → ESP32 Arduino → ESP32 Dev Module)*

5. Select the correct COM port and click **Upload**

6. Open **Serial Monitor** at `115200` baud

### Current Code

See [`src/main.cpp`](src/main.cpp) for the current working sketch.

---

## Challenges & Debugging Log

### IMU Instability
- Communication works briefly then crashes
- Investigating: wiring integrity, power supply noise, I2C pull-up resistors
- See [`docs/debugging.md`](docs/debugging.md) for running notes

### Hardware Reliability
- Current breadboard setup is not robust enough for in-water use
- Next step: solder connections → evaluate custom PCB design

### Waterproofing *(future)*
- Will need a fully sealed enclosure
- Must preserve signal accuracy and sensor calibration

---

## Roadmap

### Short Term
- [ ] Fix IMU crash / I2C instability
- [ ] Confirm stable, continuous sensor reads
- [ ] Solder connections for reliability

### Medium Term
- [ ] Log real accelerometer + gyro data
- [ ] Begin identifying swim-specific motion patterns
- [ ] Prototype basic stroke detection algorithm

### Long Term
- [ ] Compact wearable form factor
- [ ] Stroke detection & lap counting
- [ ] Performance metrics + efficiency scoring
- [ ] Bluetooth data transmission
- [ ] Mobile app integration

---

## Repo Structure

```
swim-tracker/
├── src/              # Firmware and Python scripts
│   ├── main.cpp      # ESP32 Arduino sketch
│   └── visualizer.py # Real-time Python visualizer
├── docs/             # Notes, debugging logs, research
├── hardware/         # Schematics, wiring diagrams
├── data/             # Sample captured data (CSV, logs)
└── README.md
```

---

## What I'm Learning

- Embedded systems debugging
- I2C sensor interfacing
- Soldering and hardware reliability
- Real-time data visualization with Python
- Hardware reliability & design tradeoffs
- Signal processing fundamentals *(upcoming)*
- PCB design *(upcoming)*

---

## Author

**Jun** — Electrical & Computer Systems Engineering student  
GitHub: [@ijun30225](https://github.com/ijun30225)  
Building this to learn through doing. Contributions, suggestions, and feedback welcome.
