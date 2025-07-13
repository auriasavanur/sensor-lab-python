from moku.instruments import Oscilloscope
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Moku:Go connection
scope = Oscilloscope('192.168.1.100')  # Replace with actual device IP
data = scope.get_data()
voltage = data['ch1']
time_axis = data['time']

# Preprocessing: Normalize voltage
voltage = voltage - np.mean(voltage)

# Find pulse peaks (assuming ~1Hz rate)
peaks, _ = find_peaks(voltage, height=0.2, distance=100)
peak_times = time_axis[peaks]

# Estimate BPM
intervals = np.diff(peak_times)
bpm = 60 / np.mean(intervals) if len(intervals) > 0 else 0

# Plot pulse waveform
plt.figure(figsize=(10, 5))
plt.plot(time_axis, voltage, label='Pulse Signal')
plt.plot(peak_times, voltage[peaks], "rx", label='Detected Peaks')
plt.title(f'Pulse Sensor Output — BPM: {bpm:.1f}')
plt.xlabel('Time (s)')
plt.ylabel('Normalized Voltage')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()