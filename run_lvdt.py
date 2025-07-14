import numpy as np
import matplotlib.pyplot as plt
import os

# 👇 Point Moku API to your instrument files
os.environ["MOKU_DATA_PATH"] = r"C:\Users\venv\Lib\site-packages\moku\data"

# 👇 Try importing Oscilloscope instrument
try:
    from moku.instruments import Oscilloscope
except ImportError:
    Oscilloscope = None

def get_mock_data():
    time_axis = np.linspace(0, 5, 500)
    displacement = 10 * np.sin(2 * np.pi * time_axis / 5)
    return time_axis, displacement

def main(ip, is_streamlit=False):
    scale_factor = 0.5  # mm per volt

    try:
        if ip.lower() == "demo" or ip.strip() == "":
            time_axis, displacement = get_mock_data()
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

            # 👇 Convert raw waveform to NumPy arrays
            data = scope.get_data()
            voltage = np.array(data['ch1'])
            time_axis = np.array(data['time'])

            # 👇 Filter out any zero-voltage readings
            valid = voltage != 0
            voltage = voltage[valid]
            time_axis = time_axis[valid]

            displacement = voltage * scale_factor
            mode = f"Live Mode ({ip})"

        else:
            raise RuntimeError("Oscilloscope not available")

        # 👇 Plot displacement vs time
        plt.figure(figsize=(8, 4))
        plt.plot(time_axis, displacement, label='Displacement (mm)', color='purple')
        plt.title(f'LVDT Displacement – {mode}')
        plt.xlabel('Time (s)')
        plt.ylabel('Displacement (mm)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # 👇 Display or save plot
        if is_streamlit:
            import streamlit as st
            st.pyplot(plt)
        else:
            plt.savefig("lvdt_output.png")
            print("Plot saved as lvdt_output.png")

    except Exception as e:
        print(f"Error: {e}")