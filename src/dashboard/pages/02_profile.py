import streamlit as st
import plotly.graph_objects as go
from src.dashboard.utils.db import get_companies, get_ratios

st.title("Corporate Performance Dashboard")
st.markdown("---")

companies_df = get_companies()
company_options = [f"{row['company_id']} - {row['company_name']}" for idx, row in companies_df.iterrows()]

search_query = st.selectbox("Search Company Ticker / Identity Key", options=[""] + company_options)

if search_query:
    target_id = search_query.split(" - ")[0]
    comp_meta = companies_df[companies_df['company_id'] == target_id].iloc[0]
    df_history = get_ratios(target_id)
    df_latest = df_history.sort_values(by='year').iloc[-1]

    st.subheader(comp_meta['company_name'])
    st.markdown(f"**Sector:** {comp_meta['broad_sector']} | **Sub-Sector:** {comp_meta['sub_sector']} | **NSE Ticker:** {comp_meta['nse_ticker']}")
    st.caption(comp_meta['about'])
    st.markdown("---")

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("ROE", f"{df_latest['roe']:.2f}%")
    k2.metric("ROCE", f"{df_latest['roce']:.2f}%")
    k3.metric("Net Profit Margin", f"{df_latest['npm']:.2f}%")
    k4.metric("D/E", f"{df_latest['debt_to_equity']:.2f}")
    k5.metric("Revenue CAGR 5yr", f"{df_latest['revenue_cagr_5yr']:.2f}%")
    k6.metric("FCF (latest year)", f"{df_latest['fcf']:.1f}")

    st.markdown("---")

    df_history = df_history.sort_values(by='year')
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df_history['year'], y=df_history['revenue'], name='Revenue'))
    fig_bar.add_trace(go.Bar(x=df_history['year'], y=df_history['net_profit'], name='Net Profit'))
    fig_bar.update_layout(title="10-Year Revenue and Net Profit Trend", barmode='group', hovermode='x unified')
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=df_history['year'], y=df_history['roe'], name='ROE', mode='lines+markers', yaxis='y1'))
    fig_line.add_trace(go.Scatter(x=df_history['year'], y=df_history['roce'], name='ROCE', mode='lines+markers', yaxis='y2'))
    fig_line.update_layout(
        title="ROE and ROCE Dual-Axis Trend Over 10 Years",
        xaxis=dict(title="Year"),
        yaxis=dict(title="ROE %", titlefont=dict(color="#1f77b4"), tickfont=dict(color="#1f77b4")),
        yaxis2=dict(title="ROCE %", titlefont=dict(color="#ff7f0e"), tickfont=dict(color="#ff7f0e"), overlaying='y', side='right'),
        hovermode='x unified'
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    st.subheader("Pros & Cons Analysis")
    
    p1, p2 = st.columns(2)
    with p1:
        if df_latest['roe'] > 15:
            st.markdown("🟩 **Pro:** High capital efficiency with ROE exceeding 15% system benchmarks.")
        if df_latest['debt_to_equity'] < 0.5:
            st.markdown("🟩 **Pro:** Robust balance sheet configuration with conservative leverage profile.")
        if df_latest['npm'] > 10:
            st.markdown("🟩 **Pro:** Strong pricing power with competitive advantage net margin threshold.")
            
    with p2:
        if df_latest['pe'] > 40:
            st.markdown("🟥 **Con:** Premium multiple risk with high valuation expansion requirements.")
        if df_latest['debt_to_equity'] > 2.0:
            st.markdown("🟥 **Con:** Elevated leverage concentration introducing risk profile concerns.")
        if df_latest['fcf'] < 0:
            st.markdown("🟥 **Con:** Negative cash flow production patterns eating into working capital cash reserves.")
else:
    st.info("Ticker not found — please try another")