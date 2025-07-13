import numpy as np
import matplotlib.pyplot as plt

# Try importing Moku only if available
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
            scope = Oscilloscope(ip)
            data = scope.get_data()
            voltage = data['ch1']
            time_axis = data['time']
            R_sensor = R_fixed * (V_in / voltage - 1)
            temperature = (R_sensor - R0) / (alpha * R0)
            mode = f"Live Mode ({ip})"
        else:
            raise RuntimeError("Moku:Go module not available")

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