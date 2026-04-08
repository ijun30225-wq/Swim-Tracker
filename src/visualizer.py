import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

PORT = "/dev/cu.usbserial-0001"  # Mac: check in Arduino IDE -> Tools -> Port
# Windows it'll be something like "COM3"

BAUD = 115200
MAX_POINTS = 200

ser = serial.Serial(PORT, BAUD, timeout=1)

ax_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
ay_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)
az_data = deque([0]*MAX_POINTS, maxlen=MAX_POINTS)

fig, ax = plt.subplots()
line_ax, = ax.plot([], [], label="ax")
line_ay, = ax.plot([], [], label="ay")
line_az, = ax.plot([], [], label="az")
ax.set_ylim(-20, 20)
ax.set_xlim(0, MAX_POINTS)
ax.legend()
ax.set_title("ICM20948 Acceleration (m/s²)")

def update(frame):
    if ser.in_waiting:
        try:
            line = ser.readline().decode("utf-8").strip()
            values = line.split(",")
            if len(values) == 6:
                ax_data.append(float(values[0]))
                ay_data.append(float(values[1]))
                az_data.append(float(values[2]))
                line_ax.set_data(range(MAX_POINTS), ax_data)
                line_ay.set_data(range(MAX_POINTS), ay_data)
                line_az.set_data(range(MAX_POINTS), az_data)
        except:
            pass
    return line_ax, line_ay, line_az

ani = animation.FuncAnimation(fig, update, interval=25)
plt.tight_layout()
plt.show()
