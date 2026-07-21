import os
import pandas as pd

os.makedirs("output", exist_ok=True)

FINANCIALS_PATH = "data/financials.xlsx"
RATIOS_PATH = "output/ratios_calculated.csv"
OUTPUT_PATH = "output/pros_cons_generated.csv"

def load_data():
    if os.path.exists(RATIOS_PATH):
        df_ratios = pd.read_csv(RATIOS_PATH)
    else:
        df_ratios = pd.DataFrame()
        
    if os.path.exists(FINANCIALS_PATH):
        df_fin = pd.read_excel(FINANCIALS_PATH)
    else:
        df_fin = pd.DataFrame()
        
    return df_ratios, df_fin

def evaluate_company_rules(company_id, df_c):
    results = []
    
    roe_latest = df_c["roe"].iloc[-1] if "roe" in df_c and len(df_c) > 0 else 0
    fcf_vals = df_c["fcf"].tolist() if "fcf" in df_c else []
    de_latest = df_c["debt_to_equity"].iloc[-1] if "debt_to_equity" in df_c and len(df_c) > 0 else 0
    rev_cagr_5 = df_c["revenue_cagr_5yr"].iloc[-1] if "revenue_cagr_5yr" in df_c and len(df_c) > 0 else 0
    pat_cagr_5 = df_c["pat_cagr_5yr"].iloc[-1] if "pat_cagr_5yr" in df_c and len(df_c) > 0 else 0
    eps_cagr_5 = df_c["eps_cagr_5yr"].iloc[-1] if "eps_cagr_5yr" in df_c and len(df_c) > 0 else 0
    opm_latest = df_c["opm"].iloc[-1] if "opm" in df_c and len(df_c) > 0 else 0
    icr_latest = df_c["icr"].iloc[-1] if "icr" in df_c and len(df_c) > 0 else 0
    div_yield = df_c["div_yield"].iloc[-1] if "div_yield" in df_c and len(df_c) > 0 else 0
    pat_latest = df_c["net_profit"].iloc[-1] if "net_profit" in df_c and len(df_c) > 0 else 0
    roce_latest = df_c["roce"].iloc[-1] if "roce" in df_c and len(df_c) > 0 else 0
    payout_latest = df_c["payout_ratio"].iloc[-1] if "payout_ratio" in df_c and len(df_c) > 0 else 0
    net_debt_ebitda = df_c["net_debt_ebitda"].iloc[-1] if "net_debt_ebitda" in df_c and len(df_c) > 0 else 0
    is_financial = df_c["sector"].iloc[-1].lower() in ["finance", "banking", "financial services"] if "sector" in df_c and len(df_c) > 0 else False

    if roe_latest > 20:
        results.append({"type": "pro", "rule_id": "P1", "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency", "confidence_pct": 85})
    
    if len(fcf_vals) >= 5 and all(x > 0 for x in fcf_vals[-5:]):
        results.append({"type": "pro", "rule_id": "P2", "text": "Strong free cash flow generation over 5 years signals healthy business fundamentals", "confidence_pct": 90})

    if de_latest == 0:
        results.append({"type": "pro", "rule_id": "P3", "text": "Debt-free balance sheet provides financial flexibility and eliminates interest burden", "confidence_pct": 95})

    if rev_cagr_5 > 15:
        results.append({"type": "pro", "rule_id": "P4", "text": "Revenue growing at above 15% CAGR over 5 years reflects strong business momentum", "confidence_pct": 80})

    if opm_latest > 25:
        results.append({"type": "pro", "rule_id": "P5", "text": "Operating profit margin above 25% indicates strong pricing power and cost discipline", "confidence_pct": 85})

    if pat_cagr_5 > 20:
        results.append({"type": "pro", "rule_id": "P6", "text": "Net profit compounding at above 20% over 5 years creates significant shareholder value", "confidence_pct": 85})

    if icr_latest > 10 or de_latest == 0:
        results.append({"type": "pro", "rule_id": "P7", "text": "Very high interest coverage ratio reflects negligible financial stress from debt servicing", "confidence_pct": 80})

    if div_yield > 2 and len(fcf_vals) > 0 and fcf_vals[-1] > 0:
        results.append({"type": "pro", "rule_id": "P8", "text": "Consistent dividend yield above 2% backed by positive free cash flow", "confidence_pct": 75})

    if eps_cagr_5 > 15:
        results.append({"type": "pro", "rule_id": "P9", "text": "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding", "confidence_pct": 80})

    if "roe" in df_c and len(df_c["roe"]) >= 3 and df_c["roe"].iloc[-1] > df_c["roe"].iloc[-2] > df_c["roe"].iloc[-3]:
        results.append({"type": "pro", "rule_id": "P10", "text": "Return on equity improving for 3 consecutive years shows strengthening business quality", "confidence_pct": 75})

    if rev_cagr_5 < pat_cagr_5 and rev_cagr_5 > 0:
        results.append({"type": "pro", "rule_id": "P11", "text": "Revenue growing slower than profits shows improving operating leverage and scale benefits", "confidence_pct": 70})

    if "assets" in df_c and "borrowings" in df_c and len(df_c) >= 2:
        if df_c["assets"].iloc[-1] > df_c["assets"].iloc[0] and df_c["borrowings"].iloc[-1] < df_c["borrowings"].iloc[0]:
            results.append({"type": "pro", "rule_id": "P12", "text": "Growing asset base funded by internal accruals reflects self-sustaining growth", "confidence_pct": 85})

    if not is_financial and de_latest > 2.0:
        results.append({"type": "con", "rule_id": "C1", "text": f"Debt-to-equity ratio of {de_latest:.2f} is elevated for a non-financial company and warrants monitoring", "confidence_pct": 90})

    if len(fcf_vals) >= 3 and all(x < 0 for x in fcf_vals[-3:]):
        results.append({"type": "con", "rule_id": "C2", "text": "Free cash flow negative for 3 consecutive years raises concern about cash generation quality", "confidence_pct": 85})

    if "opm" in df_c and len(df_c["opm"]) >= 3 and df_c["opm"].iloc[-1] < df_c["opm"].iloc[-2] < df_c["opm"].iloc[-3]:
        results.append({"type": "con", "rule_id": "C3", "text": "Operating margins declining for 3 consecutive years suggest pricing or cost pressure", "confidence_pct": 80})

    if pat_latest < 0:
        results.append({"type": "con", "rule_id": "C4", "text": "Company reported a net loss in the most recent financial year", "confidence_pct": 95})

    if "revenue" in df_c and len(df_c["revenue"]) >= 3 and df_c["revenue"].iloc[-1] < df_c["revenue"].iloc[-2] < df_c["revenue"].iloc[-3]:
        results.append({"type": "con", "rule_id": "C5", "text": "Revenue contraction over 2 consecutive years indicates demand weakness or market share loss", "confidence_pct": 85})

    if icr_latest < 1.5 and de_latest > 0:
        results.append({"type": "con", "rule_id": "C6", "text": "Interest coverage ratio below 1.5x indicates the company is at risk of not meeting its debt obligations", "confidence_pct": 90})

    if payout_latest > 100:
        results.append({"type": "con", "rule_id": "C7", "text": "Dividend payout ratio above 100% means the company is paying dividends from reserves, which is unsustainable", "confidence_pct": 80})

    if "debt_to_equity" in df_c and len(df_c["debt_to_equity"]) >= 3 and df_c["debt_to_equity"].iloc[-1] > df_c["debt_to_equity"].iloc[-2] > df_c["debt_to_equity"].iloc[-3]:
        results.append({"type": "con", "rule_id": "C8", "text": "Rising debt-to-equity ratio over 3 years suggests increasing financial leverage risk", "confidence_pct": 75})

    if "eps" in df_c and len(df_c["eps"]) >= 3 and df_c["eps"].iloc[-1] < df_c["eps"].iloc[-2] < df_c["eps"].iloc[-3]:
        results.append({"type": "con", "rule_id": "C9", "text": "Earnings per share declining for 3 consecutive years reflects deteriorating profitability", "confidence_pct": 80})

    if roce_latest < 10 and roce_latest != 0:
        results.append({"type": "con", "rule_id": "C10", "text": "Return on capital employed below 10% suggests the business is not generating sufficient returns on invested capital", "confidence_pct": 75})

    if net_debt_ebitda > 3:
        results.append({"type": "con", "rule_id": "C11", "text": "Net debt exceeding 3 times EBITDA is a high leverage ratio and limits financial flexibility", "confidence_pct": 85})

    if rev_cagr_5 < 5 and rev_cagr_5 != 0:
        results.append({"type": "con", "rule_id": "C12", "text": "Revenue growing at below 5% over 5 years lags inflation and suggests limited business momentum", "confidence_pct": 70})

    if not any(r["type"] == "pro" for r in results):
        results.append({"type": "pro", "rule_id": "P_DEFAULT", "text": "Maintains operational presence and ongoing corporate reporting compliance", "confidence_pct": 65})
        
    if not any(r["type"] == "con" for r in results):
        results.append({"type": "con", "rule_id": "C_DEFAULT", "text": "Subject to broader sector headwinds and macroeconomic valuation shifts", "confidence_pct": 65})

    return results

def generate_pros_cons():
    df_ratios, df_fin = load_data()
    
    if df_ratios.empty and df_fin.empty:
        pd.DataFrame(columns=["company_id", "type", "rule_id", "text", "confidence_pct"]).to_csv(OUTPUT_PATH, index=False)
        return

    source_df = df_ratios if not df_ratios.empty else df_fin
    companies = source_df["company_id"].unique() if "company_id" in source_df else []

    all_records = []

    for cid in companies:
        df_c = source_df[source_df["company_id"] == cid]
        rules_output = evaluate_company_rules(cid, df_c)
        
        for item in rules_output:
            if item["confidence_pct"] > 60:
                all_records.append({
                    "company_id": cid,
                    "type": item["type"],
                    "rule_id": item["rule_id"],
                    "text": item["text"],
                    "confidence_pct": item["confidence_pct"]
                })

    df_out = pd.DataFrame(all_records)
    df_out.to_csv(OUTPUT_PATH, index=False)

if __name__ == "__main__":
    generate_pros_cons()