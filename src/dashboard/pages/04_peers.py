import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.dashboard.utils.db import get_companies, get_sectors, get_peers, get_ratios

st.title("Peer Comparison Analytics Matrix")
st.markdown("---")

sectors = get_sectors()
selected_sector = st.selectbox("Select Target Sector Universe", sectors)

peer_companies = get_peers(selected_sector)
company_list = [f"{row['company_id']} - {row['company_name']}" for idx, row in peer_companies.iterrows()]

selected_comp_str = st.selectbox("Select Target Benchmark Company", company_list)

if selected_comp_str:
    target_id = selected_comp_str.split(" - ")[0]
    
    peer_data = []
    for idx, row in peer_companies.iterrows():
        r_df = get_ratios(row['company_id'])
        if not r_df.empty:
            latest = r_df.sort_values(by='year').iloc[-1].to_dict()
            latest['company_name'] = row['company_name']
            peer_data.append(latest)
            
    df_peers = pd.DataFrame(peer_data)
    
    radar_metrics = ['roe', 'roce', 'npm', 'opm', 'revenue_cagr_5yr', 'pat_cagr_5yr', 'asset_turnover', 'dividend_payout']
    
    target_row = df_peers[df_peers['company_id'] == target_id].iloc[0]
    peer_averages = df_peers[radar_metrics].mean()
    
    target_values = [target_row[m] for m in radar_metrics]
    avg_values = [peer_averages[m] for m in radar_metrics]
    
    target_values.append(target_values[0])
    avg_values.append(avg_values[0])
    radar_metrics.append(radar_metrics[0])
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=target_values,
        theta=radar_metrics,
        fill='toself',
        name=target_row['company_name']
    ))
    fig.add_trace(go.Scatterpolar(
        r=avg_values,
        theta=radar_metrics,
        fill='toself',
        name=f"{selected_sector} Sector Average"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=f"Cross-Sectional Vector Profile: {target_row['company_name']} vs Peer Cohort"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Cross-Sectional Sector Metric Grid")
    
    def highlight_target(row):
        return ['background-color: #1e3d59; color: white' if row['company_id'] == target_id else '' for _ in row]
        
    display_grid = df_peers[['company_id', 'company_name', 'roe', 'roce', 'npm', 'debt_to_equity', 'pe', 'pb', 'market_cap']]
    st.dataframe(
        display_grid.style.apply(highlight_target, axis=1),
        hide_index=True,
        use_container_width=True
    )