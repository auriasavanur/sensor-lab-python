import numpy as np
import matplotlib.pyplot as plt
import os

# 👇 Tell Moku API where to find instrument files
os.environ["MOKU_DATA_PATH"] = r"C:\Users\venv\Lib\site-packages\moku\data"

# 👇 Try importing the Oscilloscope class
try:
    from moku.instruments import Oscilloscope
except ImportError:
    Oscilloscope = None

def get_mock_data():
    time_axis = np.linspace(0, 5, 500)
    temperature = 25 + 5 * np.sin(2 * np.pi * time_axis / 5)
    return time_axis, temperature

def main(ip, is_streamlit=False):
    R_fixed = 1000
    V_in = 3.3
    R0 = 100
    alpha = 0.00385

    try:
        if ip.lower() == "demo" or ip.strip() == "":
            time_axis, temperature = get_mock_data()
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

            # 👇 Acquire data and convert to NumPy arrays for calculation
            data = scope.get_data()
            voltage = np.array(data['ch1'])
            time_axis = np.array(data['time'])

            # 👇 Calculate temperature from voltage
            R_sensor = R_fixed * ((V_in / voltage) - 1)
            temperature = (R_sensor - R0) / (alpha * R0)
            mode = f"Live Mode ({ip})"

        else:
            raise RuntimeError("Oscilloscope not available")

        # 👇 Plotting
        plt.figure(figsize=(8, 4))
        plt.plot(time_axis, temperature, label='Temperature (°C)', color='blue')
        plt.title(f'RTD Temperature Output – {mode}')
        plt.xlabel('Time (s)')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        if is_streamlit:
            import streamlit as st
            st.pyplot(plt)
        else:
            plt.savefig("rtd_output.png")
            print("Plot saved as rtd_output.png")

    except Exception as e:
        print(f"Error: {e}")