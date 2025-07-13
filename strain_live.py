from moku.instruments import Oscilloscope
import numpy as np
import matplotlib.pyplot as plt

# Bridge Constants
V_in = 2.0              # CH2 excitation voltage
R_fixed = 350           # Reference resistor in bridge
gain = 100              # Amplifier gain for microstrain
conversion_factor = 1   # Optional calibration scaling

# Connect to Moku:Go
scope = Oscilloscope('192.168.1.100')  # Update IP if needed
data = scope.get_data()
voltage = data['ch1']
time_axis = data['time']

# Estimate strain from voltage (simplified)
microstrain = gain * voltage * conversion_factor

# Plot strain
plt.plot(time_axis, microstrain, label='Microstrain')
plt.title('Strain Gauge Output')
plt.xlabel('Time (s)')
plt.ylabel('Strain (µε)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()