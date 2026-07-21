import os
import re
import pandas as pd

os.makedirs("output", exist_ok=True)

ANALYSIS_EXCEL_PATH = "data/analysis.xlsx"
PARSED_OUTPUT_PATH = "output/analysis_parsed.csv"
FAILURES_OUTPUT_PATH = "output/parse_failures.csv"

TARGET_FIELDS = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

REGEX_PATTERN = re.compile(r"(\d+)\s*Years?:?\s*(-?[\d.]+)%", re.IGNORECASE)

def parse_analysis_text():
    if not os.path.exists(ANALYSIS_EXCEL_PATH):
        pd.DataFrame(columns=["company_id", "metric_type", "period_years", "value_pct"]).to_csv(PARSED_OUTPUT_PATH, index=False)
        pd.DataFrame(columns=["company_id", "field", "raw_text", "reason"]).to_csv(FAILURES_OUTPUT_PATH, index=False)
        return

    df_analysis = pd.read_excel(ANALYSIS_EXCEL_PATH)
    
    parsed_records = []
    failure_records = []

    for _, row in df_analysis.iterrows():
        company_id = row.get("company_id")
        
        for field in TARGET_FIELDS:
            if field not in row or pd.isna(row[field]):
                continue
            
            raw_text = str(row[field]).strip()
            matches = REGEX_PATTERN.findall(raw_text)
            
            if matches:
                for period_str, val_str in matches:
                    try:
                        parsed_records.append({
                            "company_id": company_id,
                            "metric_type": field,
                            "period_years": int(period_str),
                            "value_pct": float(val_str)
                        })
                    except ValueError:
                        failure_records.append({
                            "company_id": company_id,
                            "field": field,
                            "raw_text": raw_text,
                            "reason": f"Conversion error for ({period_str}, {val_str})"
                        })
            else:
                failure_records.append({
                    "company_id": company_id,
                    "field": field,
                    "raw_text": raw_text,
                    "reason": "Regex pattern mismatch"
                })

    pd.DataFrame(parsed_records).to_csv(PARSED_OUTPUT_PATH, index=False)
    pd.DataFrame(failure_records).to_csv(FAILURES_OUTPUT_PATH, index=False)

def cross_validate_cagr():
    if not os.path.exists(PARSED_OUTPUT_PATH):
        return
    
    df_parsed = pd.read_csv(PARSED_OUTPUT_PATH)
    if df_parsed.empty:
        return

    cagr_5yr = df_parsed[df_parsed["period_years"] == 5]

if __name__ == "__main__":
    parse_analysis_text()
    cross_validate_cagr()