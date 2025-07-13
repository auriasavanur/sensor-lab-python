import numpy as np
import matplotlib.pyplot as plt

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
            scope = Oscilloscope(ip)
            data = scope.get_data()
            voltage = data['ch1']
            time_axis = data['time']
            strain = voltage / (gauge_factor * V_in)
            mode = f"Live Mode ({ip})"
        else:
            raise RuntimeError("Moku:Go module not available")

        plt.figure(figsize=(8, 4))
        plt.plot(time_axis, strain, label='Strain (ε)', color='green')
        plt.title(f'Strain Gauge Output – {mode}')
        plt.xlabel('Time (s)')
        plt.ylabel('Strain (ε)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        if is_streamlit:
            import streamlit as st
            st.pyplot(plt)
        else:
            plt.savefig("strain_output.png")
            print("Plot saved as strain_output.png")

    except Exception as e:
        print(f"Error: {e}")