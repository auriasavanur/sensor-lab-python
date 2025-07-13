import streamlit as st
import run_rtd
import run_strain
import run_lvdt
import run_pulse

st.set_page_config(page_title="Sensor Lab Dashboard", layout="centered")

st.title("📘 Sensor Lab Training GUI")
st.subheader("Run Python-Powered Experiments with Moku:Go")

experiment = st.selectbox("Choose an experiment to run:", [
    "RTD / Thermistor Calibration",
    "Strain Gauge Output",
    "LVDT Displacement",
    "Pulse Sensor Visualization",
    "FFT Analysis (Coming Soon)",
    "Accelerometer Integration (Coming Soon)"
])

ip_address = st.text_input("Enter Moku:Go IP Address", "192.168.1.100")
start_button = st.button("▶ Start Experiment")

# QR Preview Section
if experiment == "RTD / Thermistor Calibration":
    st.image("images/qr_codes/rtd_qr.png", caption="Scan to view RTD script", width=200)
elif experiment == "Strain Gauge Output":
    st.image("images/qr_codes/strain_qr.png", caption="Scan to view Strain Gauge script", width=200)
elif experiment == "LVDT Displacement":
    st.image("images/qr_codes/lvdt_qr.png", caption="Scan to view LVDT script", width=200)
elif experiment == "Pulse Sensor Visualization":
    st.image("images/qr_codes/pulse_qr.png", caption="Scan to view Pulse Sensor script", width=200)

# Button logic
if start_button:
    if "Coming Soon" in experiment:
        st.warning(f"{experiment} is under development and will be available in a future release.")
    else:
        st.success(f"Launching {experiment}...")
        try:
            if experiment == "RTD / Thermistor Calibration":
                run_rtd.main(ip_address, is_streamlit=True)
            elif experiment == "Strain Gauge Output":
                run_strain.main(ip_address, is_streamlit=True)
            elif experiment == "LVDT Displacement":
                run_lvdt.main(ip_address, is_streamlit=True)
            elif experiment == "Pulse Sensor Visualization":
                run_pulse.main(ip_address, is_streamlit=True)
            else:
                st.error("Module script not found.")
        except Exception as e:
            st.error(f"Failed to run script: {e}")