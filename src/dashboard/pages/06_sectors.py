import streamlit as st
import pandas as pd
import plotly.express as px
from src.dashboard.utils.db import get_companies, get_sectors, get_peers, get_ratios

st.title("Multidimensional Sector Space Analysis")
st.markdown("---")

sectors = get_sectors()
selected_sector = st.selectbox("Select Target Sector for Cross-Sectional Map", sectors)

if selected_sector:
    peer_companies = get_peers(selected_sector)
    sector_data = []
    
    for idx, row in peer_companies.iterrows():
        r_df = get_ratios(row['company_id'])
        if not r_df.empty:
            latest = r_df.sort_values(by='year').iloc[-1].to_dict()
            latest['company_name'] = row['company_name']
            latest['sub_sector'] = row['sub_sector']
            sector_data.append(latest)
            
    if sector_data:
        df_sector = pd.DataFrame(sector_data)
        
        st.subheader(f"Relative Valuation vs. Efficiency Map: {selected_sector}")
        
        fig = px.scatter(
            df_sector,
            x='pe',
            y='roe',
            size='market_cap',
            color='sub_sector',
            hover_name='company_name',
            labels={
                'pe': 'P/E Ratio (Valuation)',
                'roe': 'Return on Equity (%)',
                'market_cap': 'Market Cap (Cr)',
                'sub_sector': 'Sub-Sector Grouping'
            },
            title="Return on Equity vs P/E Ratio (Bubble Size = Market Cap)"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Sub-Sector Benchmark Summary Tables")
        
        grouped = df_sector.groupby('sub_sector').agg({
            'company_id': 'count',
            'roe': 'mean',
            'pe': 'mean',
            'debt_to_equity': 'mean',
            'market_cap': 'sum'
        }).reset_index()
        
        grouped.columns = ['Sub-Sector Group', 'Companies', 'Average ROE (%)', 'Average P/E', 'Average D/E', 'Total Market Cap (Cr)']
        st.dataframe(grouped, hide_index=True, use_container_width=True)
    else:
        st.warning("No financial history records found for the selected sector.")