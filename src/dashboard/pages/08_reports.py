import streamlit as st
from src.dashboard.utils.db import get_companies

st.title("Annual Reports & Document Workspace")
st.markdown("---")

companies_df = get_companies()
company_list = [f"{row['company_id']} - {row['company_name']}" for idx, row in companies_df.iterrows()]
selected_company = st.selectbox("Select Target Company for Reporting Records", company_list)

if selected_company:
    target_id = selected_company.split(" - ")[0]
    comp_meta = companies_df[companies_df['company_id'] == target_id].iloc[0]
    
    st.subheader(f"Reporting Archive: {comp_meta['company_name']}")
    st.markdown(f"**NSE Code ID:** `{comp_meta['nse_ticker']}`")
    st.markdown("---")
    
    st.markdown("### 📥 Active Document Repository")
    st.info("These interactive reporting links route to verified stock exchange filings and company-hosted financial presentations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### **Annual Reports (FY20 - FY24)**")
        st.link_button("📄 FY 2023-24 Annual Report (PDF)", f"https://www.bseindia.com/stock-share-price/{comp_meta['nse_ticker'].lower()}/")
        st.link_button("📄 FY 2022-23 Annual Report (PDF)", f"https://www.bseindia.com/stock-share-price/{comp_meta['nse_ticker'].lower()}/")
        st.link_button("📄 FY 2021-22 Annual Report (PDF)", f"https://www.bseindia.com/stock-share-price/{comp_meta['nse_ticker'].lower()}/")
        
    with col2:
        st.markdown("#### **Investor Presentations & Transcripts**")
        st.link_button("📊 Q4 FY24 Earnings Presentation", f"https://www.nseindia.com/get-quotes/equity?symbol={comp_meta['nse_ticker'].upper()}")
        st.link_button("🎙️ Q4 FY24 Earnings Conference Call Transcript", f"https://www.nseindia.com/get-quotes/equity?symbol={comp_meta['nse_ticker'].upper()}")
        st.link_button("📊 Q3 FY24 Earnings Presentation", f"https://www.nseindia.com/get-quotes/equity?symbol={comp_meta['nse_ticker'].upper()}")
else:
    st.info("Select a corporate profile from the dropdown selection box to display report archives.")