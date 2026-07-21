import os
import pandas as pd

os.makedirs("output", exist_ok=True)

CAPITAL_ALLOC_PATH = "output/capital_allocation.csv"
CASHFLOW_INTEL_PATH = "output/cashflow_intelligence.xlsx"
PATTERN_CHANGES_PATH = "output/pattern_changes.csv"

def process_capital_allocation_report():
    if os.path.exists(CAPITAL_ALLOC_PATH):
        df_alloc = pd.read_csv(CAPITAL_ALLOC_PATH)
    else:
        df_alloc = pd.DataFrame(columns=["company_id", "year", "pattern"])

    if df_alloc.empty:
        pd.DataFrame(columns=["company_id", "previous_year", "previous_pattern", "latest_year", "latest_pattern"]).to_csv(PATTERN_CHANGES_PATH, index=False)
        return

    df_alloc = df_alloc.sort_values(by=["company_id", "year"])
    
    latest_years = df_alloc.groupby("company_id")["year"].transform("max")
    df_latest = df_alloc[df_alloc["year"] == latest_years].copy()
    
    distribution_summary = df_latest["pattern"].value_counts().to_dict()

    if os.path.exists(CASHFLOW_INTEL_PATH):
        try:
            df_intel = pd.read_excel(CASHFLOW_INTEL_PATH)
            pattern_map = dict(zip(df_latest["company_id"], df_latest["pattern"]))
            df_intel["sprint2_capital_pattern"] = df_intel["company_id"].map(pattern_map).fillna("Unclassified")
            df_intel.to_excel(CASHFLOW_INTEL_PATH, index=False)
        except Exception:
            pass

    pattern_changes = []
    companies = df_alloc["company_id"].unique()

    for cid in companies:
        df_c = df_alloc[df_alloc["company_id"] == cid]
        if len(df_c) >= 2:
            prev_row = df_c.iloc[-2]
            last_row = df_c.iloc[-1]
            
            if prev_row["pattern"] != last_row["pattern"]:
                pattern_changes.append({
                    "company_id": cid,
                    "previous_year": int(prev_row["year"]),
                    "previous_pattern": prev_row["pattern"],
                    "latest_year": int(last_row["year"]),
                    "latest_pattern": last_row["pattern"]
                })

    df_changes = pd.DataFrame(pattern_changes)
    if df_changes.empty:
        df_changes = pd.DataFrame(columns=["company_id", "previous_year", "previous_pattern", "latest_year", "latest_pattern"])
    
    df_changes.to_csv(PATTERN_CHANGES_PATH, index=False)

if __name__ == "__main__":
    process_capital_allocation_report()