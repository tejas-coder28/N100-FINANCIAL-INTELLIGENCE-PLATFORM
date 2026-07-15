import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.dashboard.utils.db import get_companies, get_ratios

st.title("Corporate Capital Allocation Strategy")
st.markdown("---")

companies_df = get_companies()
company_list = [f"{row['company_id']} - {row['company_name']}" for idx, row in companies_df.iterrows()]
selected_company = st.selectbox("Select Target Company to Analyze Capital Allocation", company_list)

if selected_company:
    target_id = selected_company.split(" - ")[0]
    df_history = get_ratios(target_id).sort_values(by='year')
    
    if not df_history.empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_history['year'],
            y=df_history['fcf'],
            name='Free Cash Flow (FCF)',
            marker_color='#2ca02c'
        ))
        fig.add_trace(go.Scatter(
            x=df_history['year'],
            y=df_history['dividend_payout'],
            name='Dividend Payout %',
            mode='lines+markers',
            yaxis='y2',
            line=dict(color='#ff7f0e', width=3)
        ))
        fig.update_layout(
            title="Free Cash Flow generation vs. Dividend Payout Policies",
            xaxis=dict(title="Year"),
            yaxis=dict(title="FCF (Cr)", title_font=dict(color="#2ca02c"), tickfont=dict(color="#2ca02c")),
            yaxis2=dict(
                title="Dividend Payout Ratio (%)",
                title_font=dict(color="#ff7f0e"),
                tickfont=dict(color="#ff7f0e"),
                overlaying='y',
                side='right',
                range=[0, 100]
            ),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Capital Allocation Profiling Table")
        
        display_cols = ['year', 'fcf', 'dividend_yield', 'dividend_payout', 'debt_to_equity', 'interest_coverage_ratio']
        df_alloc = df_history[display_cols].copy()
        df_alloc.columns = ['Year', 'FCF (Cr)', 'Dividend Yield (%)', 'Dividend Payout (%)', 'D/E Ratio', 'Interest Coverage']
        st.dataframe(df_alloc, hide_index=True, use_container_width=True)
else:
    st.info("Select a corporate listing above to load capital reinvestment profiles.")