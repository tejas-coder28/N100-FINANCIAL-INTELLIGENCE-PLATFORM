import csv
import os

def compute_free_cash_flow(operating_activity: float, investing_activity: float) -> float:
    return operating_activity + investing_activity

def compute_cfo_quality_score(cfo_5yr_avg: float, pat_5yr_avg: float) -> tuple:
    if pat_5yr_avg == 0:
        return None, "Accrual Risk"
    ratio = cfo_5yr_avg / pat_5yr_avg
    if ratio > 1.0:
        return round(ratio, 2), "High Quality"
    elif 0.5 <= ratio <= 1.0:
        return round(ratio, 2), "Moderate"
    else:
        return round(ratio, 2), "Accrual Risk"

def compute_capex_intensity(investing_activity: float, sales: float) -> tuple:
    if sales == 0:
        return None, "Asset Light"
    intensity = (abs(investing_activity) / sales) * 100
    if intensity < 3.0:
        return round(intensity, 2), "Asset Light"
    elif 3.0 <= intensity <= 8.0:
        return round(intensity, 2), "Moderate"
    else:
        return round(intensity, 2), "Capital Intensive"

def compute_fcf_conversion_rate(fcf: float, operating_profit: float) -> float:
    if operating_profit == 0:
        return None
    return (fcf / operating_profit) * 100

def classify_capital_allocation_pattern(cfo: float, cfi: float, cff: float, cfo_5yr_avg: float = None, pat_5yr_avg: float = None) -> str:
    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"
    
    pattern = (cfo_sign, cfi_sign, cff_sign)
    
    if pattern == ("+", "-", "-"):
        if cfo_5yr_avg is not None and pat_5yr_avg is not None and pat_5yr_avg != 0:
            if (cfo_5yr_avg / pat_5yr_avg) > 1.0:
                return "Shareholder Returns"
        return "Reinvestor"
    elif pattern == ("+", "+", "-"):
        return "Liquidating Assets"
    elif pattern == ("-", "+", "+"):
        return "Distress Signal"
    elif pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"
    elif pattern == ("+", "+", "+"):
        return "Cash Accumulator"
    elif pattern == ("-", "-", "-"):
        return "Pre-Revenue"
    elif pattern == ("+", "-", "+"):
        return "Mixed"
    return "Mixed"

def generate_capital_allocation_report(data_rows, output_path="output/capital_allocation.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["company_id", "year", "cfo_sign", "cfi_sign", "cff_sign", "pattern_label"])
        for row in data_rows:
            cfo_sign = "+" if row["cfo"] >= 0 else "-"
            cfi_sign = "+" if row["cfi"] >= 0 else "-"
            cff_sign = "+" if row["cff"] >= 0 else "-"
            label = classify_capital_allocation_pattern(row["cfo"], row["cfi"], row["cff"], row.get("cfo_5yr"), row.get("pat_5yr"))
            writer.writerow([row["company_id"], row["year"], cfo_sign, cfi_sign, cff_sign, label])