# Debugging Log

Running notes on issues hit during development and how they were resolved.

---

## [Resolved] ICM20948 returning zero values for magnetometer

**Symptom:** Accel and gyro data looked correct in Serial Monitor, but mx/my/mz were always 0.

**Cause:** The ICM20948 contains two separate chips: the main IMU (accel + gyro) and a magnetometer chip called the AK09916. They communicate over their own internal I2C bus. The main chip initializes quickly; the AK09916 takes longer to come online.

**Fix:** Added `delay(500)` after `icm.begin_I2C()` before the main loop starts. This gives the magnetometer enough time to wake up.

---

## [Resolved] Python visualizer showing all zeros, then sudden data spike

**Symptom:** The live plot was flat at zero for most of the session, then real data appeared suddenly near the end of the window.

**Cause:** Arduino Serial Monitor and the Python script were both trying to use the same serial port. The OS only allows one program to hold a serial port at a time. Serial Monitor had it locked, so Python was getting nothing. When Serial Monitor was closed, Python finally received data — but by then, the serial buffer had a large backlog that dumped all at once.

**Fix:** Close Serial Monitor completely before running `visualizer.py`. They are mutually exclusive.

---

## [Resolved] Serial buffer backlog at 100Hz

**Symptom:** Even without the Serial Monitor conflict, data appeared delayed and inconsistent. The plot looked choppy.

**Cause:** The Arduino was sending data at 100Hz (10ms delay). Python's plot redraw takes non-trivial time, so it couldn't keep up. The serial buffer accumulated a backlog faster than Python could drain it.

**Fix:** Slowed the Arduino loop to 50Hz (`delay(20)`). The Python script already drains the full buffer each iteration, so 50Hz is smooth and there's no buildup.

---

## [Resolved] I2C instability / sensor crashing

**Symptom:** Sensor would communicate briefly then stop responding or produce garbage values.

**Cause:** I2C lines need pull-up resistors to 3.3V. Without them, the bus floats and behavior is unreliable — especially as wire lengths increase or the sensor moves.

**Fix:** Added 5.1kΩ pull-up resistors on both SDA and SCL lines to 3.3V. Stable ever since.

---

## [Open] Breadboard reliability for in-water use

**Issue:** Breadboard connections work fine on the bench but would not survive submersion or physical stress from swimming.

**Plan:**
- Solder all connections to perfboard or a custom PCB
- Evaluate conformal coating or silicone enclosure for waterproofing
- Test physical durability before any in-water trials
