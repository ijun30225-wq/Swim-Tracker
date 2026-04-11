"""
Real-time IMU Visualizer
------------------------
Reads ICM20948 data from the ESP32 over serial and plots it live.

IMPORTANT: Close the Arduino Serial Monitor before running this script.
           Only one program can hold the serial port at a time.

Usage:
    python visualizer.py

Output:
    - Live matplotlib window (4 subplots)
    - CSV file saved on close: imu_log_YYYYMMDD_HHMMSS.csv

Install dependencies:
    pip install pyserial matplotlib pandas
"""

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from collections import deque
import serial
import time
import pandas as pd
from datetime import datetime

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
PORT = "/dev/cu.usbserial-0001"  # macOS example
#PORT = "COM3"                   # Windows example
#PORT = "/dev/ttyUSB0"           # Linux example
BAUD = 115200
MAX_POINTS = 300  # Rolling window size (number of samples visible at once)


# -------------------------------------------------------------------
# Serial setup
# -------------------------------------------------------------------
print(f"Opening {PORT}...")
ser = serial.Serial(PORT, BAUD, timeout=0.1)
time.sleep(2)
ser.reset_input_buffer()
print(f"Connected to {PORT}\n")


# -------------------------------------------------------------------
# Data buffers
# -------------------------------------------------------------------
# deque with maxlen acts as a rolling window:
# new data is appended to the right, old data falls off the left automatically.
ax_data = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)
ay_data = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)
az_data = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)
gx_data = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)
gy_data = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)
gz_data = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)
mx_data = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)
my_data = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)
mz_data = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)
mag_acc = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)  # |accel| magnitude
mag_gyr = deque([0] * MAX_POINTS, maxlen=MAX_POINTS)  # |gyro| magnitude

log_data = []  # All samples, saved to CSV on exit
start_time = time.time()


# -------------------------------------------------------------------
# Plot setup
# -------------------------------------------------------------------
plt.ion()  # Interactive mode: allows live updates without blocking
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("ICM20948 Live Data", fontsize=14)

x_axis = list(range(MAX_POINTS))

def setup_subplot(axis, title, ylim, labels, colors):
    axis.set_title(title)
    axis.set_ylim(*ylim)
    axis.set_xlim(0, MAX_POINTS)
    axis.grid(True, alpha=0.3)
    lines = [axis.plot(x_axis, [0] * MAX_POINTS, c, label=l, linewidth=1.5)[0]
             for l, c in zip(labels, colors)]
    axis.legend(loc='upper right')
    return lines

(line_ax, line_ay, line_az) = setup_subplot(
    ax1, "Acceleration (m/s²)", (-20, 20), ["X", "Y", "Z"], ["r-", "g-", "b-"]
)
(line_gx, line_gy, line_gz) = setup_subplot(
    ax2, "Gyroscope (rad/s)", (-5, 5), ["X", "Y", "Z"], ["r-", "g-", "b-"]
)
(line_mx, line_my, line_mz) = setup_subplot(
    ax3, "Magnetometer (µT)", (-100, 150), ["X", "Y", "Z"], ["r-", "g-", "b-"]
)
(line_mag_acc, line_mag_gyr) = setup_subplot(
    ax4, "Motion Intensity", (0, 30), ["|Accel|", "|Gyro|"], ["b-", "r-"]
)

plt.tight_layout()
plt.show(block=False)
print("Live plotting active. Move the sensor to see data.")
print("Close the plot window to stop and save.\n")


# -------------------------------------------------------------------
# Main loop
# -------------------------------------------------------------------
frame_count = 0

try:
    while True:
        if not plt.fignum_exists(fig.number):
            break

        data_received = False

        # Drain everything in the serial buffer before redrawing.
        # This prevents the buffer from building up a backlog.
        for _ in range(ser.in_waiting + 10):
            if not ser.in_waiting:
                break
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()

                # Skip blank lines and header/debug text (lines starting with a letter)
                if not line or line[0].isalpha():
                    continue

                values = line.split()
                if len(values) != 9:
                    continue

                ax, ay, az = float(values[0]), float(values[1]), float(values[2])
                gx, gy, gz = float(values[3]), float(values[4]), float(values[5])
                mx, my, mz = float(values[6]), float(values[7]), float(values[8])

                ax_data.append(ax); ay_data.append(ay); az_data.append(az)
                gx_data.append(gx); gy_data.append(gy); gz_data.append(gz)
                mx_data.append(mx); my_data.append(my); mz_data.append(mz)
                mag_acc.append((ax**2 + ay**2 + az**2) ** 0.5)
                mag_gyr.append((gx**2 + gy**2 + gz**2) ** 0.5)

                log_data.append([time.time() - start_time, ax, ay, az, gx, gy, gz, mx, my, mz])
                frame_count += 1
                data_received = True

            except (ValueError, UnicodeDecodeError):
                pass  # Malformed line — skip it

        # Only redraw the plot if new data arrived this cycle
        if data_received:
            x_vals = list(range(MAX_POINTS))

            line_ax.set_data(x_vals, list(ax_data))
            line_ay.set_data(x_vals, list(ay_data))
            line_az.set_data(x_vals, list(az_data))

            line_gx.set_data(x_vals, list(gx_data))
            line_gy.set_data(x_vals, list(gy_data))
            line_gz.set_data(x_vals, list(gz_data))

            line_mx.set_data(x_vals, list(mx_data))
            line_my.set_data(x_vals, list(my_data))
            line_mz.set_data(x_vals, list(mz_data))

            line_mag_acc.set_data(x_vals, list(mag_acc))
            line_mag_gyr.set_data(x_vals, list(mag_gyr))

            fig.canvas.draw()
            fig.canvas.flush_events()

            if frame_count % 50 == 0:
                print(f"Samples: {frame_count:5d} | "
                      f"Accel Z: {az:6.2f} m/s² | "
                      f"Gyro X: {gx:6.2f} rad/s | "
                      f"Mag Z: {mz:7.2f} µT")

        plt.pause(0.01)

except KeyboardInterrupt:
    print("\nStopped.")
except Exception as e:
    print(f"\nError: {e}")
finally:
    ser.close()
    if log_data:
        filename = f"imu_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df = pd.DataFrame(log_data, columns=[
            "timestamp", "ax", "ay", "az", "gx", "gy", "gz", "mx", "my", "mz"
        ])
        df.to_csv(filename, index=False)
        elapsed = time.time() - start_time
        print(f"Saved {len(log_data)} samples to {filename}")
        print(f"Average sample rate: {len(log_data) / elapsed:.1f} Hz")
    else:
        print("No data collected.")
    plt.close()
