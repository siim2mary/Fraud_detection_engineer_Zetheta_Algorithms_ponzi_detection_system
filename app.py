import streamlit as st
import pandas as pd
import numpy as np
import json
import os

# --- Page Configuration ---
st.set_page_config(page_title="Ponzi Security Dashboard", layout="wide")

st.title("🛡️ Smart Ponzi Detection Engine")
st.markdown("""
This dashboard identifies high-risk smart contracts by analyzing their economic structure and transaction behavior.
""")

# --- Sidebar: User Input for Real-time Check ---
st.sidebar.header("Manual Contract Audit")
gini = st.sidebar.slider("Gini Index (Wealth Concentration)", 0.0, 1.0, 0.5)
paid_rate = st.sidebar.slider("Paid Rate (Payout Ratio)", 0.0, 1.0, 0.2)
velocity = st.sidebar.number_input("Transaction Velocity (Daily)", min_value=0, value=100)
growth = st.sidebar.slider("Network Growth Rate", 0.0, 5.0, 1.2)

# Simple Prediction Logic (Heuristic for demo)
risk_score = (gini * 40) + ((1 - paid_rate) * 40) + (min(velocity/500, 1) * 20)
risk_score = min(risk_score, 100)

if st.sidebar.button("Analyze Contract"):
    st.sidebar.write(f"### Result: {risk_score:.2f}% Risk")
    if risk_score > 75:
        st.sidebar.error("🚨 CRITICAL: Ponzi Signature Detected")
    elif risk_score > 40:
        st.sidebar.warning("⚠️ HIGH: Suspicious Activity")
    else:
        st.sidebar.success("✅ LOW: Healthy Patterns")

# --- Main Dashboard: Analytics ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Metric Overview")
    st.metric(label="Total Scanned", value="758", delta="12 new")
    st.metric(label="Critical Blocked", value="40", delta="3", delta_color="inverse")

with col2:
    st.subheader("Detection Triggers")
    # Displaying the feature importance from your engine
    chart_data = pd.DataFrame({
        'Feature': ['Gini Index', 'Paid Rate', 'Velocity', 'Growth'],
        'Importance': [0.35, 0.40, 0.15, 0.10]
    })
    st.bar_chart(chart_data.set_index('Feature'))

# --- Data Table: Recent Alerts ---
st.subheader("Recent Firewall Alerts")
try:
    with open('outputs/firewall_blocklist.json', 'r') as f:
        blocklist = json.load(f)
        st.write(f"There are currently **{len(blocklist)}** addresses on the real-time blocklist.")
        st.table(pd.DataFrame({"Address Index": blocklist}).head(10))
except FileNotFoundError:
    st.info("No active blocklist found. Run 'engine.py' first to generate logs.")