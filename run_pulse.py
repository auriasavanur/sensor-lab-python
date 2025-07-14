import numpy as np
import matplotlib.pyplot as plt
import os

# 👇 Point Moku API to the correct instrument data path
os.environ["MOKU_DATA_PATH"] = r"C:\Users\venv\Lib\site-packages\moku\data"

# 👇 Import Oscilloscope safely
try:
    from moku.instruments import Oscilloscope
except ImportError:
    Oscilloscope = None

def get_mock_data():
    time_axis = np.linspace(0, 5, 500)
    pulse = 1 + 0.5 * np.sin(2 * np.pi * time_axis * 1.2)
    return time_axis, pulse

def main(ip, is_streamlit=False):
    try:
        if ip.lower() == "demo" or ip.strip() == "":
            time_axis, pulse = get_mock_data()
            mode = "Demo Mode"

        elif Oscilloscope:
            scope = Oscilloscope(
                ip,
                force_connect=True,
                ignore_busy=True,
                persist_state=False,
                connect_timeout=10,
                read_timeout=10
            )

            # 👇 Convert voltage and time to NumPy arrays
            data = scope.get_data()
            pulse = np.array(data['ch1'])
            time_axis = np.array(data['time'])

            # 👇 Filter out zero voltages to keep waveform stable
            valid = pulse != 0
            pulse = pulse[valid]
            time_axis = time_axis[valid]

            mode = f"Live Mode ({ip})"

        else:
            raise RuntimeError("Oscilloscope not available")

        # 👇 Plot pulse waveform
        plt.figure(figsize=(8, 4))
        plt.plot(time_axis, pulse, label='Pulse Signal', color='red')
        plt.title(f'Pulse Sensor Output – {mode}')
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        if is_streamlit:
            import streamlit as st
            st.pyplot(plt)
        else:
            plt.savefig("pulse_output.png")
            print("Plot saved as pulse_output.png")

    except Exception as e:
        print(f"Error: {e}")