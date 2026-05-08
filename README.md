# 🛡️ AI-Powered Cyberthreat Analyzer & SOC Dashboard

[![Live Demo](https://img.shields.io/badge/Live_Demo-Click_Here-blue?style=for-the-badge)](https://satwik-1204.github.io/CyberGermanicus/)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/ML-XGBoost_%7C_Scikit--Learn-orange?style=for-the-badge)](#)

An industry-grade, dual-engine network intrusion detection system built on the **CICIDS2017** dataset. This project simulates a real-time Security Operations Center (SOC) environment, analyzing network packets to intercept both known volumetric attacks and zero-day anomalies.

---

## 🧠 The Architecture: Two-Tiered Defense

Modern cybersecurity requires hybrid AI systems. A single model is insufficient for catching both loud network floods and stealthy, novel probes. This engine utilizes a tiered approach:

### 🛑 Tier 1: The Frontline (XGBoost Classifier)
* **Role:** Detects known, high-volume threats with extreme accuracy.
* **Performance:** **99.99% accuracy** in intercepting volumetric DDoS attacks by identifying specific packet-size fingerprints (e.g., `fwd_packet_length_mean`).
* **Logic:** Acts as the primary filter. If a known signature is detected, the packet is instantly blocked.

### 🕵️‍♂️ Tier 2: The Zero-Day Scout (Isolation Forest)
* **Role:** Unsupervised anomaly detection.
* **Performance:** Trained exclusively on benign network baselines (`contamination=0.01`). 
* **Logic:** If traffic passes Tier 1, it is evaluated here. The model ignores loud floods and specifically flags the top 1% most statistically unusual packets that bypass standard signatures, alerting on potential zero-day vulnerabilities.

---

## 🛠️ Data Engineering Pipeline

Handling massive cybersecurity datasets requires strict memory and feature optimization:
* **Memory Optimization:** Converted 10GB+ of raw PCAP `.csv` data into highly optimized `.parquet` formats using PyArrow, preventing RAM overflow during training and drastically speeding up I/O operations.
* **Feature Selection:** Calculated correlation matrices to identify and drop 26 highly collinear network features (threshold > 0.95), optimizing model inference time and preventing overfitting.
* **Preprocessing:** Handled extreme class imbalances and scaled high-dimensional data using `StandardScaler` to prepare for unsupervised clustering.

---

## 🚀 The Live SOC Simulation

This repository includes a live HTML/JS dashboard simulation that visualizes the AI engine's decision-making process in real-time. 

👉 **[Launch the Live Dashboard](https://satwik-1204.github.io/CyberGermanicus/)**

**Simulation Features:**
* **Dynamic Sampling:** Continuously injects benign traffic to establish a baseline.
* **Volumetric Spikes:** Simulates massive DDoS floods to trigger Tier 1 XGBoost defenses.
* **Zero-Day Injection:** Simulates novel anomalies to trigger Tier 2 Isolation Forest defenses.
* **Real-time Metrics:** Tracks packets scanned, threats blocked, and safe traffic allowed.

---

## 💻 Tech Stack

* **Machine Learning:** `Scikit-Learn`, `XGBoost`
* **Data Processing:** `Pandas`, `NumPy`, `PyArrow` (Parquet)
* **Frontend Simulation:** HTML5, CSS3, JavaScript, `Chart.js`

---

## 👨‍💻 Author

**Satwik Ghosh**
* [GitHub Profile](https://github.com/Satwik-1204)
