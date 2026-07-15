import streamlit as st
import pandas as pd
from src.dashboard.utils.db import get_companies, get_ratios

st.title("Dynamic Strategy Screener Engine")
st.markdown("---")

companies_df = get_companies()
all_data = []
for idx, row in companies_df.iterrows():
    r_df = get_ratios(row['company_id'])
    if not r_df.empty:
        latest = r_df.sort_values(by='year').iloc[-1].to_dict()
        latest['company_name'] = row['company_name']
        latest['sector'] = row['broad_sector']
        all_data.append(latest)

master_df = pd.DataFrame(all_data)

st.sidebar.subheader("Strategy Presets")
p_cols = st.sidebar.columns(2)
preset_quality = p_cols[0].button("Quality")
preset_value = p_cols[0].button("Value")
preset_growth = p_cols[0].button("Growth")
preset_dividend = p_cols[1].button("Dividend")
preset_debtfree = p_cols[1].button("Debt-Free")
preset_turnaround = p_cols[1].button("Turnaround")

init_values = {
    "roe_min": 5.0, "de_max": 3.0, "fcf_min": -100.0,
    "rev_min": 0.0, "pat_min": 0.0, "opm_min": 5.0,
    "pe_max": 80.0, "pb_max": 15.0, "div_min": 0.0, "icr_min": 1.5
}

if preset_quality:
    init_values.update({"roe_min": 20.0, "de_max": 0.5, "opm_min": 18.0})
elif preset_value:
    init_values.update({"pe_max": 15.0, "pb_max": 2.0, "roe_min": 12.0})
elif preset_growth:
    init_values.update({"rev_min": 15.0, "pat_min": 15.0, "roe_min": 15.0})
elif preset_dividend:
    init_values.update({"div_min": 3.0, "pe_max": 25.0, "de_max": 1.0})
elif preset_debtfree:
    init_values.update({"de_max": 0.05, "icr_min": 20.0})
elif preset_turnaround:
    init_values.update({"rev_min": 10.0, "fcf_min": 200.0, "roe_min": 6.0})

st.sidebar.subheader("Metric Filter Sliders")
roe_filter = st.sidebar.slider("Minimum ROE (%)", 5.0, 35.0, init_values["roe_min"])
de_filter = st.sidebar.slider("Maximum D/E Ratio", 0.0, 8.0, init_values["de_max"])
fcf_filter = st.sidebar.slider("Minimum FCF (Cr)", -100.0, 1500.0, init_values["fcf_min"])
rev_filter = st.sidebar.slider("Minimum 5Yr Rev CAGR (%)", 0.0, 30.0, init_values["rev_min"])
pat_filter = st.sidebar.slider("Minimum 5Yr PAT CAGR (%)", 0.0, 35.0, init_values["pat_min"])
opm_filter = st.sidebar.slider("Minimum OPM (%)", 5.0, 40.0, init_values["opm_min"])
pe_filter = st.sidebar.slider("Maximum P/E Ratio", 8.0, 80.0, init_values["pe_max"])
pb_filter = st.sidebar.slider("Maximum P/B Ratio", 0.5, 15.0, init_values["pb_max"])
div_filter = st.sidebar.slider("Minimum Dividend Yield (%)", 0.0, 5.0, init_values["div_min"])
icr_filter = st.sidebar.slider("Minimum Interest Coverage Ratio", 1.5, 25.0, init_values["icr_min"])

filtered_df = master_df[
    (master_df['roe'] >= roe_filter) &
    (master_df['debt_to_equity'] <= de_filter) &
    (master_df['fcf'] >= fcf_filter) &
    (master_df['revenue_cagr_5yr'] >= rev_filter) &
    (master_df['pat_cagr_5yr'] >= pat_filter) &
    (master_df['opm'] >= opm_filter) &
    (master_df['pe'] <= pe_filter) &
    (master_df['pb'] <= pb_filter) &
    (master_df['dividend_yield'] >= div_filter) &
    (master_df['interest_coverage_ratio'] >= icr_filter)
]

st.markdown(f"### **{len(filtered_df)}** companies match your filters")

display_cols = [
    'company_id', 'company_name', 'sector', 'composite_quality_score',
    'roe', 'debt_to_equity', 'fcf', 'revenue_cagr_5yr', 'pat_cagr_5yr',
    'opm', 'pe', 'pb', 'dividend_yield', 'interest_coverage_ratio'
]
st.dataframe(filtered_df[display_cols], hide_index=True, use_container_width=True)

csv_data = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
st.download_button(
    label="Export Result Set to CSV",
    data=csv_data,
    file_name="screener_output.csv",
    mime="text/csv"
)