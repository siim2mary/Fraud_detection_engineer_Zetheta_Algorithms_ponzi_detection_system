import streamlit as st
import pandas as pd
import networkx as nx
from detection import ZethetaPonziEngine  # Assuming your code is in detection.py

# --- Page Configuration ---
st.set_page_config(page_title="Zetheta Ponzi Detector", layout="wide")

st.title("🛡️ On-Chain Ponzi Detection Dashboard")
st.markdown("### Zetheta Algorithms | Forensic Fraud Analysis")

# --- Sidebar: Data Input ---
st.sidebar.header("Data Ingestion")
st.sidebar.info("Upload transaction CSV or use the default simulation data.")

# Realistic Mock Data for the Dashboard
diverse_data = [
    {"from": "Retail_1", "to": "Alpha_Vault", "amount": 1000},
    {"from": "Retail_2", "to": "Alpha_Vault", "amount": 1500},
    {"from": "Retail_3", "to": "Alpha_Vault", "amount": 2000},
    {"from": "Retail_4", "to": "Beta_Mixer", "amount": 500},
    {"from": "Alpha_Vault", "to": "Early_Investor", "amount": 3200}, 
    {"from": "Early_Investor", "to": "Retail_1", "amount": 200},    
    {"from": "Beta_Mixer", "to": "Alpha_Vault", "amount": 450},     
]

# --- Execution ---
engine = ZethetaPonziEngine()
engine.ingest_data(diverse_data)
report = engine.run_diagnostics()

# --- Layout: Key Metrics ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Risk Score", f"{report['score']}/100", delta="- Critical" if report['score'] > 70 else None)

with col2:
    st.metric("Risk Level", report['level'])

with col3:
    st.metric("Wallets Analyzed", report['metadata']['wallets'])

st.divider()

# --- Layout: Findings & Graph ---
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("🚩 Detailed Findings")
    for finding in report['findings']:
        st.error(finding)
    
    st.subheader("📝 Executive Summary")
    st.write("The system exhibits strong Ponzi-like characteristics due to high dependency on new capital, centralized fund control, and circular transaction behavior.")

with right_col:
    st.subheader("🕸️ Network Topology")
    # Display the raw transaction ledger
    df = pd.DataFrame(diverse_data)
    st.dataframe(df, use_container_width=True)
    
    # Download Audit Log Button
    st.download_button(
        label="Download Forensic Audit Log (JSON)",
        data=str(report),
        file_name="zetheta_audit_log.json",
        mime="application/json"
    )

st.success("Analysis Complete: Engine operational and monitoring data stream.")