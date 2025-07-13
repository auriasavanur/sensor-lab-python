from moku.instruments import Oscilloscope
import numpy as np
import matplotlib.pyplot as plt

# RTD Constants
R_fixed = 1000       # Ω
V_in = 3.3           # Input voltage
R0 = 100             # RTD resistance @ 0°C
alpha = 0.00385      # RTD coefficient

# Connect to Moku:Go
scope = Oscilloscope('192.168.1.100')  # Replace with your actual IP
data = scope.get_data()
voltage = data['ch1']
time_axis = data['time']

# Convert voltage to resistance, then to temperature
R_sensor = R_fixed * (V_in / voltage - 1)
temperature = (R_sensor - R0) / (alpha * R0)

# Plot temperature
plt.plot(time_axis, temperature, label='Temperature (°C)')
plt.title('RTD Temperature Output')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()