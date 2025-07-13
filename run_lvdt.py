import numpy as np
import matplotlib.pyplot as plt

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
            scope = Oscilloscope(ip)
            data = scope.get_data()
            voltage = data['ch1']
            time_axis = data['time']
            displacement = voltage * scale_factor
            mode = f"Live Mode ({ip})"
        else:
            raise RuntimeError("Moku:Go module not available")

        plt.figure(figsize=(8, 4))
        plt.plot(time_axis, displacement, label='Displacement (mm)', color='purple')
        plt.title(f'LVDT Displacement – {mode}')
        plt.xlabel('Time (s)')
        plt.ylabel('Displacement (mm)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        if is_streamlit:
            import streamlit as st
            st.pyplot(plt)
        else:
            plt.savefig("lvdt_output.png")
            print("Plot saved as lvdt_output.png")

    except Exception as e:
        print(f"Error: {e}")