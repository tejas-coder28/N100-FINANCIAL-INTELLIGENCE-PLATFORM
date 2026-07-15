import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.dashboard.utils.db import get_companies, get_ratios

st.title("Historical Trend & YoY Growth Engine")
st.markdown("---")

companies_df = get_companies()
company_list = [f"{row['company_id']} - {row['company_name']}" for idx, row in companies_df.iterrows()]
selected_company = st.selectbox("Select Target Company to Analyze Trends", company_list)

if selected_company:
    target_id = selected_company.split(" - ")[0]
    df_history = get_ratios(target_id).sort_values(by='year')
    
    metrics_to_plot = st.multiselect(
        "Select Metrics to Overlay",
        options=['roe', 'roce', 'npm', 'opm', 'debt_to_equity', 'interest_coverage_ratio', 'asset_turnover'],
        default=['roe', 'roce']
    )
    
    if metrics_to_plot and not df_history.empty:
        fig = go.Figure()
        for metric in metrics_to_plot:
            fig.add_trace(go.Scatter(
                x=df_history['year'],
                y=df_history[metric],
                mode='lines+markers',
                name=metric.upper()
            ))
        fig.update_layout(
            title="Multi-Metric Historical Performance Overlay",
            xaxis=dict(title="Year"),
            yaxis=dict(title="Metric Value / Percentage"),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Automated YoY Growth & Performance Insights")
        
        for metric in metrics_to_plot:
            val_earliest = df_history[metric].iloc[0]
            val_latest = df_history[metric].iloc[-1]
            diff = val_latest - val_earliest
            
            if diff > 0:
                st.write(f"🟩 **{metric.upper()}** expanded from **{val_earliest:.2f}%** to **{val_latest:.2f}%** over the tracking horizon (a net increase of **+{diff:.2f}%**).")
            else:
                st.write(f"🟥 **{metric.upper()}** compressed from **{val_earliest:.2f}%** to **{val_latest:.2f}%** over the tracking horizon (a net decrease of **{diff:.2f}%**).")
else:
    st.info("Please select a target corporate entity to trigger the historical trend engine.")