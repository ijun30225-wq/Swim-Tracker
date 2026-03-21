# Debugging Log

Running notes on issues encountered and steps taken to resolve them.

---

## Issue 1 — IMU Crash / I2C Instability

**Date:** *(fill in)*  
**Status:** 🔴 Open

### Symptoms
- I2C communication initializes successfully
- Valid data received for a short period
- System crashes after a short runtime

### Hypotheses
- [ ] Loose wiring / poor contact on breadboard
- [ ] Insufficient or noisy power supply (ESP32 3.3V rail drooping under load)
- [ ] Missing or incorrectly valued I2C pull-up resistors (4.7kΩ recommended)
- [ ] I2C clock speed too high — try reducing to 100kHz (`Wire.setClock(100000)`)
- [ ] Wrong I2C pins — ESP32 defaults are SDA=GPIO21, SCL=GPIO22
- [ ] IMU register bank not selected correctly (ICM-20948 uses bank switching)
- [ ] Watchdog timer reset — ESP32 WDT fires if loop() blocks too long

### Steps Taken
- *(Document what you've tried here)*

### Resolution
- *(Fill in once solved)*

---

*Add new issues below as they come up.*
