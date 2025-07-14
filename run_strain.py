import numpy as np
import matplotlib.pyplot as plt
import os

# 👇 Set the instrument file path for Moku API
os.environ["MOKU_DATA_PATH"] = r"C:\Users\venv\Lib\site-packages\moku\data"

# 👇 Import Oscilloscope from Moku API
try:
    from moku.instruments import Oscilloscope
except ImportError:
    Oscilloscope = None

def get_mock_data():
    time_axis = np.linspace(0, 5, 500)
    strain = 0.02 * np.sin(2 * np.pi * time_axis / 5)
    return time_axis, strain

def main(ip, is_streamlit=False):
    gauge_factor = 2.0
    V_in = 3.3

    try:
        if ip.lower() == "demo" or ip.strip() == "":
            time_axis, strain = get_mock_data()
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

            # 👇 Convert raw data to NumPy arrays
            data = scope.get_data()
            voltage = np.array(data['ch1'])
            time_axis = np.array(data['time'])

            # 👇 Filter out invalid voltage readings (e.g., zero)
            valid = voltage != 0
            voltage = voltage[valid]
            time_axis = time_axis[valid]

            # 👇 Compute strain signal
            strain = voltage / (gauge_factor * V_in)
            mode = f"Live Mode ({ip})"

        else:
            raise RuntimeError("Oscilloscope not available")

        # 👇 Plotting setup
        plt.figure(figsize=(8, 4))
        plt.plot(time_axis, strain, label='Strain (ε)', color='green')
        plt.title(f'Strain Gauge Output – {mode}')
        plt.xlabel('Time (s)')
        plt.ylabel('Strain (ε)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # 👇 Output
        if is_streamlit:
            import streamlit as st
            st.pyplot(plt)
        else:
            plt.savefig("strain_output.png")
            print("Plot saved as strain_output.png")

    except Exception as e:
        print(f"Error: {e}")