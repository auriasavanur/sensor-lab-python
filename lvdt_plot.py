from moku.instruments import Oscilloscope
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

# Moku:Go connection
scope = Oscilloscope('192.168.1.100')  # Replace with correct IP
data = scope.get_data()
voltage = data['ch1']
time_axis = data['time']

# Envelope detection (LVDT secondary output)
analytic_signal = hilbert(voltage)
envelope = np.abs(analytic_signal)

# Normalize for relative displacement (simulation only)
displacement_mm = envelope / np.max(envelope) * 10  # Assuming ±10 mm range

# Plot displacement
plt.plot(time_axis, displacement_mm, label='Displacement (mm)')
plt.title('LVDT Output Simulation')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (mm)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()