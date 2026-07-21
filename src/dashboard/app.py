import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

DB_PATH = "data/financial_analytics.db"
RAW_DIR = "data/raw"
TEARSHEET_DIR = "reports/tearsheets"

st.set_page_config(
    page_title="N100 Financial Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    comp_path = os.path.join(RAW_DIR, "companies.xlsx")
    sec_path = os.path.join(RAW_DIR, "sectors.xlsx")
    rat_path = os.path.join(RAW_DIR, "financial_ratios.xlsx")

    df_comp = pd.read_excel(comp_path) if os.path.exists(comp_path) else pd.DataFrame()
    df_sec = pd.read_excel(sec_path) if os.path.exists(sec_path) else pd.DataFrame()
    df_rat = pd.read_excel(rat_path) if os.path.exists(rat_path) else pd.DataFrame()

    if not df_comp.empty and not df_sec.empty and "sector_id" in df_comp.columns:
        df_comp = df_comp.merge(df_sec, on="sector_id", how="left")

    if not df_comp.empty and not df_rat.empty and "company_id" in df_comp.columns:
        df_comp = df_comp.merge(df_rat, on="company_id", how="left")

    return df_comp

df = load_data()

# Sidebar Filters
st.sidebar.title("📌 Filter Controls")

if not df.empty:
    sec_col = "sector_name" if "sector_name" in df.columns else ("sector" if "sector" in df.columns else None)
    sectors = ["All"] + sorted(list(df[sec_col].dropna().unique())) if sec_col else ["All"]
    selected_sector = st.sidebar.selectbox("Select Sector", sectors)

    filtered_df = df if selected_sector == "All" else df[df[sec_col] == selected_sector]

    cid_col = "company_id" if "company_id" in df.columns else df.columns[0]
    companies = ["All"] + sorted(list(filtered_df[cid_col].dropna().unique()))
    selected_company = st.sidebar.selectbox("Select Company Ticker/ID", companies)

    if selected_company != "All":
        filtered_df = filtered_df[filtered_df[cid_col] == selected_company]
else:
    filtered_df = pd.DataFrame()

# Header
st.title("📊 N100 Financial Intelligence Platform")
st.markdown("Interactive UI reporting for cross-company ratio exploration and PDF tearsheet management.")

# Top KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Companies Tracked", len(df["company_id"].unique()) if "company_id" in df.columns else len(df))
with col2:
    st.metric("Filtered Set Count", len(filtered_df))
with col3:
    st.metric("Sectors Represented", len(df["sector_name"].unique()) if "sector_name" in df.columns else 1)
with col4:
    pdf_count = len(os.listdir(TEARSHEET_DIR)) if os.path.exists(TEARSHEET_DIR) else 0
    st.metric("PDF Tearsheets Ready", pdf_count)

st.divider()

# Interactive Data Section
st.subheader("📋 Financial Intelligence Explorer")

if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)

    # Plotly Visuals
    col_left, col_right = st.columns(2)

    num_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    with col_left:
        st.subheader("📈 Metric Distribution")
        if num_cols:
            selected_metric = st.selectbox("Select Metric to Distribution Plot", num_cols, index=0)
            fig_hist = px.histogram(
                filtered_df, 
                x=selected_metric, 
                color="sector_name" if "sector_name" in filtered_df.columns else None,
                title=f"Distribution of {selected_metric}"
            )
            st.plotly_chart(fig_hist, use_container_width=True)

    with col_right:
        st.subheader("📊 Comparative Scatter Analysis")
        if len(num_cols) >= 2:
            x_axis = st.selectbox("X-Axis Metric", num_cols, index=0)
            y_axis = st.selectbox("Y-Axis Metric", num_cols, index=min(1, len(num_cols)-1))
            fig_scatter = px.scatter(
                filtered_df, 
                x=x_axis, 
                y=y_axis, 
                hover_data=["company_id"] if "company_id" in filtered_df.columns else None,
                color="sector_name" if "sector_name" in filtered_df.columns else None,
                title=f"{y_axis} vs {x_axis}"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    # PDF Tearsheet Download Section
    st.divider()
    st.subheader("📑 Download Executive Tearsheet")
    
    selected_cid = st.selectbox("Select Company for PDF Retrieval", sorted(df[cid_col].unique()) if cid_col in df.columns else [])
    pdf_filename = f"{selected_cid}_tearsheet.pdf"
    pdf_path = os.path.join(TEARSHEET_DIR, pdf_filename)

    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {pdf_filename}",
                data=f,
                file_name=pdf_filename,
                mime="application/pdf"
            )
    else:
        st.warning(f"No generated PDF found for {selected_cid} at `{pdf_path}`.")
else:
    st.error("No data available to display in dashboard.")