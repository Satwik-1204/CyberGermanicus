# Frontend SOC Dashboard: app.py
import streamlit as st
import pandas as pd
import numpy as np
import time
from threat_detector import SmartThreatDetector
st.set_page_config(page_title="AI SOC Dashboard", page_icon="🛡️", layout="wide")
@st.cache_resource
def load_engine():
    BASE_DIR = 'C:/Users/SATWIK GHOSH/OneDrive/Desktop/AI-Powered Cyberthreat Analyzer'
    return SmartThreatDetector(BASE_DIR), BASE_DIR
try:
    detector, base_dir = load_engine()
except Exception as e:
    st.error(f"Failed to load AI Models. Error: {e}")
    st.stop()
@st.cache_data
def load_network_data():
    return pd.read_parquet(f'{base_dir}/processed/cicids_cleaned.parquet').drop(columns=['label'])
test_data = load_network_data()
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'ddos_count' not in st.session_state:
    st.session_state.ddos_count = 0
if 'anomaly_count' not in st.session_state:
    st.session_state.anomaly_count = 0
if 'benign_count' not in st.session_state:
    st.session_state.benign_count = 0
st.title("🛡️ AI-Powered SOC Dashboard")
st.markdown("Real-Time Dual-Engine Network Intrusion Detection System")
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    batch_size = st.slider("Packets per Scan", min_value=1, max_value=50, value=10)
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Intercept & Analyze Live Traffic", use_container_width=True, type="primary")
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Dashboard", use_container_width=True):
        st.session_state.logs = []
        st.session_state.ddos_count = 0
        st.session_state.anomaly_count = 0
        st.session_state.benign_count = 0
        st.rerun()
if analyze_btn:
    with st.spinner("Analyzing network packets..."):
        simulated_stream = test_data.sample(n=batch_size, random_state=np.random.randint(0, 100000))
        verdicts = detector.analyze_traffic(simulated_stream)
        for verdict in verdicts:
            timestamp = pd.Timestamp.now().strftime("%H:%M:%S.%f")[:-3]
            if "DDoS" in verdict:
                st.session_state.ddos_count += 1
                status = "🚨 BLOCK (DDoS)"
            elif "Zero-Day" in verdict:
                st.session_state.anomaly_count += 1
                status = "⚠️ FLAG (Anomaly)"
            else:
                st.session_state.benign_count += 1
                status = "✅ ALLOW (Benign)"
            st.session_state.logs.insert(0, {"Timestamp": timestamp, "Action Taken": status, "AI Engine Details": verdict})
            if len(st.session_state.logs) > 100:
                st.session_state.logs.pop()
total_scanned = st.session_state.benign_count + st.session_state.ddos_count + st.session_state.anomaly_count
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Packets Scanned", f"{total_scanned:,}")
kpi2.metric("✅ Safe Traffic Allowed", f"{st.session_state.benign_count:,}")
kpi3.metric("🚨 DDoS Attacks Blocked", f"{st.session_state.ddos_count:,}")
kpi4.metric("⚠️ Zero-Day Anomalies", f"{st.session_state.anomaly_count:,}")
st.markdown("---")
st.subheader("📡 Live Traffic Feed")
if st.session_state.logs:
    log_df = pd.DataFrame(st.session_state.logs)
    st.dataframe(log_df, use_container_width=True, hide_index=True)
else:
    st.info("System Online. Awaiting network traffic... Click 'Intercept & Analyze' to begin.")