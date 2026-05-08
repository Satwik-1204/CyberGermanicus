# Final Production Engine: threat_detector.py
import pandas as pd
import numpy as np
import joblib
import os
import time

class SmartThreatDetector:
    def __init__(self, base_dir):
        """
        Initializes the detection engine by loading the pre-trained scaler and models.
        """
        print("[INIT] Booting up Smart Cyber Threat Detector...")
        self.models_dir = f'{base_dir}/models/'
        try:
            self.scaler = joblib.load(f'{self.models_dir}cicids_scaler.pkl')
            self.xgb_model = joblib.load(f'{self.models_dir}xgb_ddos_detector.pkl')
            self.iso_forest = joblib.load(f'{self.models_dir}isolation_forest_detector.pkl')
            self.feature_names = self.xgb_model.get_booster().feature_names
            print("[INIT] All models loaded successfully. System Online.\n")
        except FileNotFoundError as e:
            print(f"[CRITICAL ERROR] Could not find model files: {e}")
            print("Please ensure Notebooks 2, 3, and 4 ran successfully.")
            exit()
    def analyze_traffic(self, traffic_data):
        """
        The core engine. Takes a Pandas DataFrame of network traffic and returns a threat verdict.
        """
        traffic_data = traffic_data[self.feature_names]
        scaled_data = pd.DataFrame(self.scaler.transform(traffic_data), columns=self.feature_names)
        results = []
        for index, row in scaled_data.iterrows():
            row_array = pd.DataFrame([row.values], columns=self.feature_names)
            xgb_pred = self.xgb_model.predict(row_array)[0]
            if xgb_pred == 1:
                results.append("ALERT: Volumetric Attack (DDoS) Detected by Tier 1!")
                continue
            iso_pred = self.iso_forest.predict(row_array)[0]
            if iso_pred == -1:
                score = self.iso_forest.decision_function(row_array)[0]
                results.append(f"WARNING: Zero-Day Anomaly Detected by Tier 2! (Score: {score:.4f})")
            else:
                results.append("BENIGN: Traffic verified as safe.")
                
        return results
if __name__ == "__main__":
    BASE_DIR = 'C:/Users/SATWIK GHOSH/OneDrive/Desktop/AI-Powered Cyberthreat Analyzer'
    detector = SmartThreatDetector(BASE_DIR)
    print("[SIMULATION] Intercepting live network packets...")
    try:
        test_data = pd.read_parquet(f'{BASE_DIR}/processed/cicids_cleaned.parquet').drop(columns=['label'])
        simulated_stream = test_data.sample(n=5, random_state=np.random.randint(0, 1000))
        verdicts = detector.analyze_traffic(simulated_stream)
        print("-" * 60)
        print("    NETWORK TRAFFIC ANALYSIS DASHBOARD    ")
        print("-" * 60)
        for i, verdict in enumerate(verdicts):
            time.sleep(0.5)
            print(f"Packet [{i+1}/5] -> {verdict}")
        print("-" * 60)
    except Exception as e:
        print(f"[ERROR] Simulation failed: {e}")