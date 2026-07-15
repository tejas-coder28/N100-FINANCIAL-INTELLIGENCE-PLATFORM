import streamlit as st
import pandas as pd
import plotly.express as px
from src.dashboard.utils.db import get_companies, get_ratios

selected_year = st.sidebar.selectbox("Select Analysis Year", list(range(2024, 2018, -1)))

companies_df = get_companies()
all_ratios = []
for idx, row in companies_df.iterrows():
    r_df = get_ratios(row['company_id'], year=selected_year)
    if not r_df.empty:
        r_df['company_name'] = row['company_name']
        r_df['broad_sector'] = row['broad_sector']
        all_ratios.append(r_df)

if all_ratios:
    df = pd.concat(all_ratios, ignore_index=True)
else:
    df = pd.DataFrame()

st.title("Market Overview & Macro Intelligence")
st.markdown("---")

if not df.empty:
    avg_roe = df['roe'].mean()
    med_pe = df['pe'].median()
    med_de = df['debt_to_equity'].median()
    total_companies = len(df)
    med_cagr = df['revenue_cagr_5yr'].median()
    debt_free_count = (df['debt_to_equity'] < 0.1).sum()

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Average ROE", f"{avg_roe:.2f}%")
    m2.metric("Median P/E", f"{med_pe:.2f}x")
    m3.metric("Median D/E", f"{med_de:.2f}")
    m4.metric("Total Companies", f"{total_companies}")
    m5.metric("Median Revenue CAGR 5yr", f"{med_cagr:.2f}%")
    m6.metric("Debt-Free Companies", f"{debt_free_count}")

    st.markdown("---")
    c1, c2 = st.columns([2, 3])

    with c1:
        st.subheader("Sector Allocations")
        sector_counts = df['broad_sector'].value_counts().reset_index()
        sector_counts.columns = ['Sector', 'Count']
        fig = px.pie(sector_counts, names='Sector', values='Count', hole=0.4)
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Top 5 Quality Alpha Leaderboard")
        top_5 = df.sort_values(by='composite_quality_score', ascending=False).head(5)
        st.dataframe(
            top_5[['company_id', 'company_name', 'broad_sector', 'composite_quality_score', 'roe', 'pe']],
            hide_index=True,
            use_container_width=True
        )
else:
    st.warning("No tracking records identified for the selected historical metrics parameters.")