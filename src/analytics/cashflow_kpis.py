import os
import pandas as pd

os.makedirs("output", exist_ok=True)

FINANCIALS_PATH = "data/financials.xlsx"
RATIOS_PATH = "output/ratios_calculated.csv"
OUTPUT_XLSX = "output/cashflow_intelligence.xlsx"
DISTRESS_CSV = "output/distress_alerts.csv"

def load_dataset():
    if os.path.exists(RATIOS_PATH):
        return pd.read_csv(RATIOS_PATH)
    elif os.path.exists(FINANCIALS_PATH):
        return pd.read_excel(FINANCIALS_PATH)
    return pd.DataFrame()

def process_cashflow_intelligence():
    df = load_dataset()
    
    if df.empty:
        cols_xlsx = ["company_id", "sector", "cfo_quality_score", "cfo_quality_label", 
                     "capex_intensity_pct", "capex_label", "fcf_cagr_5yr", 
                     "fcf_conversion_pct", "distress_flag", "deleveraging_flag", "capital_allocation_label"]
        pd.DataFrame(columns=cols_xlsx).to_excel(OUTPUT_XLSX, index=False)
        pd.DataFrame(columns=["company_id", "cfo", "cff", "net_profit"]).to_csv(DISTRESS_CSV, index=False)
        return

    companies = df["company_id"].unique() if "company_id" in df else []
    
    records = []
    distress_alerts = []

    for cid in companies:
        df_c = df[df["company_id"] == cid].sort_values(by="year") if "year" in df else df[df["company_id"] == cid]
        
        cfo_list = df_c["cfo"].tolist() if "cfo" in df_c else []
        pat_list = df_c["net_profit"].tolist() if "net_profit" in df_c else []
        sales_list = df_c["revenue"].tolist() if "revenue" in df_c else []
        cfi_list = df_c["cfi"].tolist() if "cfi" in df_c else []
        cff_list = df_c["cff"].tolist() if "cff" in df_c else []
        fcf_list = df_c["fcf"].tolist() if "fcf" in df_c else []
        borrowings = df_c["borrowings"].tolist() if "borrowings" in df_c else []
        sector = df_c["sector"].iloc[-1] if "sector" in df_c and len(df_c) > 0 else "Unknown"

        ratios = []
        for c, p in zip(cfo_list, pat_list):
            if p != 0:
                ratios.append(c / p)
            else:
                ratios.append(0.0)
        
        recent_ratios = ratios[-5:] if len(ratios) >= 5 else ratios
        cfo_quality_score = sum(recent_ratios) / len(recent_ratios) if recent_ratios else 0.0

        if cfo_quality_score > 1.0:
            cfo_quality_label = "High Quality"
        elif cfo_quality_score >= 0.5:
            cfo_quality_label = "Moderate"
        else:
            cfo_quality_label = "Accrual Risk"

        latest_sales = sales_list[-1] if sales_list else 0
        latest_cfi = cfi_list[-1] if cfi_list else 0
        
        if latest_sales > 0:
            capex_intensity_pct = (abs(latest_cfi) / latest_sales) * 100
        else:
            capex_intensity_pct = 0.0

        if capex_intensity_pct < 3.0:
            capex_label = "Asset Light"
        elif capex_intensity_pct <= 8.0:
            capex_label = "Moderate"
        else:
            capex_label = "Capital Intensive"

        fcf_cagr_5yr = df_c["fcf_cagr_5yr"].iloc[-1] if "fcf_cagr_5yr" in df_c and len(df_c) > 0 else 0.0
        
        if latest_sales > 0 and len(fcf_list) > 0:
            fcf_conversion_pct = (fcf_list[-1] / latest_sales) * 100
        else:
            fcf_conversion_pct = 0.0

        latest_cfo = cfo_list[-1] if cfo_list else 0
        latest_cff = cff_list[-1] if cff_list else 0
        latest_pat = pat_list[-1] if pat_list else 0

        distress_flag = bool(latest_cfo < 0 and latest_cff > 0)
        
        if distress_flag:
            distress_alerts.append({
                "company_id": cid,
                "cfo": latest_cfo,
                "cff": latest_cff,
                "net_profit": latest_pat
            })

        deleveraging_flag = False
        if len(borrowings) >= 2 and len(cff_list) >= 1:
            if cff_list[-1] < 0 and borrowings[-1] < borrowings[-2]:
                deleveraging_flag = True

        if distress_flag:
            alloc_label = "Distress Signal"
        elif deleveraging_flag:
            alloc_label = "Deleveraging"
        elif capex_label == "Capital Intensive":
            alloc_label = "Aggressive Reinvestor"
        elif cfo_quality_label == "High Quality" and capex_label == "Asset Light":
            alloc_label = "Cash Generator"
        else:
            alloc_label = "Balanced Allocator"

        records.append({
            "company_id": cid,
            "sector": sector,
            "cfo_quality_score": round(cfo_quality_score, 2),
            "cfo_quality_label": cfo_quality_label,
            "capex_intensity_pct": round(capex_intensity_pct, 2),
            "capex_label": capex_label,
            "fcf_cagr_5yr": round(fcf_cagr_5yr, 2),
            "fcf_conversion_pct": round(fcf_conversion_pct, 2),
            "distress_flag": distress_flag,
            "deleveraging_flag": deleveraging_flag,
            "capital_allocation_label": alloc_label
        })

    df_out = pd.DataFrame(records)
    df_out.to_excel(OUTPUT_XLSX, index=False)

    df_distress = pd.DataFrame(distress_alerts)
    if df_distress.empty:
        df_distress = pd.DataFrame(columns=["company_id", "cfo", "cff", "net_profit"])
    df_distress.to_csv(DISTRESS_CSV, index=False)

if __name__ == "__main__":
    process_cashflow_intelligence()