import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Nifty 100 Financial Intelligence Platform")
st.markdown("---")

st.markdown("""
### Welcome to Sprint 4 Analytics System Workspace
Use the sidebar navigation links to toggle across all 8 execution screens:

1. **Home Screen** — Macro metrics overview, sector allocations, and leaderboard rankings.
2. **Company Profile** — Interactive corporate dashboards, historical trends, and dual-axis chart overlays.
3. **Screener Tool** — Live metric sliders, target strategy quick-presets, and CSV export engines.
4. **Peer Comparison** — Comparative polar coordinate performance profiles vs Peer Averages.
5. **Trend Analysis** — Multi-metric overlays with automated YoY annotations.
6. **Sector Analysis** — Cross-sectional sub-sector comparisons via multidimensional scatter metrics.
7. **Capital Allocation** — Interactive corporate capital allocation mapping.
8. **Annual Reports** — PDF linkages and corporate reporting records.
""")

st.sidebar.success("Select a screen from the page hierarchy above to begin.")