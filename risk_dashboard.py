import streamlit as st
import pandas as pd
import plotly.express as px

def run_dashboard(df, risk_score, status, alerts):
    st.title("🛡️ On-Chain Ponzi Detection Engine")
    
    # 1. High-Level Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Risk Score", f"{risk_score}/100", delta=risk_score, delta_color="inverse")
    col2.metric("Sustainability Ratio", f"{df['sustainability_ratio'].iloc[-1]:.2f}")
    col3.metric("Protocol Runway", f"{df['runway_days'].iloc[-1]:.0f} Days")

    # 2. Early Warning System Notifications
    for alert in alerts:
        st.error(alert)

    # 3. Flow Visualization (The Death Spiral Chart)
    st.subheader("Capital Flow Analysis")
    fig = px.line(df, x='timestamp', y=['new_deposits', 'yield_disbursed'], 
                  title="Inflow vs. Outflow (Ponzi Intersection)")
    st.plotly_chart(fig, use_container_width=True)

    # 4. Due Diligence Table
    st.subheader("🕵️ Wallet Concentration Audit")
    st.dataframe(df[['wallet_address', 'yield_share', 'is_insider']].sort_values(by='yield_share', ascending=False))