import streamlit as st
import pandas as pd
# Import your modules
from bitconnect_test import generate_bitconnect_data
from yield_engine import calculate_yield_health
from concentration_engine import analyze_wallet_concentration
from scoring_engine import calculate_red_flag_score
from warning_system import check_early_warnings

st.set_page_config(page_title="Zetheta Ponzi Shield", layout="wide")

# --- DATA GENERATION (Part 7) ---
df = generate_bitconnect_data()

# --- ENGINE PROCESSING (Parts 2-5) ---
df = calculate_yield_health(df)

# Get the latest stats for scoring
latest_row = df.iloc[-1]
prev_row = df.iloc[-2]

# Concentration (Part 3) - Simulating wallet list for Gini
concentration_stats = analyze_wallet_concentration(df) 

# Final Scoring (Part 4)
risk_score, risk_category = calculate_red_flag_score(
    latest_row['sustainability_ratio'], 
    concentration_stats['gini_coefficient'],
    (df['treasury_balance'].pct_change().iloc[-1]) * -1 # Decay rate
)

# Alerts (Part 5)
alerts = check_early_warnings(risk_score, prev_row.name, (df['treasury_balance'].pct_change().iloc[-1]))

# --- DASHBOARD UI (Part 6) ---
st.title("🛡️ Zetheta: On-Chain Ponzi Detection")
st.subheader(f"Status: {risk_category}")

col1, col2, col3 = st.columns(3)
col1.metric("Risk Score", f"{risk_score}/100")
col2.metric("Sustainability", f"{latest_row['sustainability_ratio']:.2f}x")
col3.metric("Gini (Concentration)", f"{concentration_stats['gini_coefficient']}")

if alerts:
    for a in alerts:
        st.warning(a)

st.line_chart(df.set_index('timestamp')[['new_deposits', 'yield_disbursed']])

st.write("### Forensic Data Logs")
st.dataframe(df.tail(10))