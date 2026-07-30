import pytest
import pandas as pd

def apply_dq_rules(df):
    failures = []
    
    # DQ-01: Company ID missing
    for idx, row in df.iterrows():
        if pd.isna(row.get("company_id")):
            failures.append({"rule_id": "DQ-01", "severity": "HIGH", "issue": "Missing company_id"})
        if pd.isna(row.get("revenue")) or row.get("revenue", 0) < 0:
            failures.append({"rule_id": "DQ-02", "severity": "HIGH", "issue": "Negative revenue"})
        if row.get("operating_margin", 0) > 100 or row.get("operating_margin", 0) < -100:
            failures.append({"rule_id": "DQ-03", "severity": "MEDIUM", "issue": "Invalid operating_margin"})
        if row.get("promoter_holding", 0) > 100 or row.get("promoter_holding", 0) < 0:
            failures.append({"rule_id": "DQ-04", "severity": "MEDIUM", "issue": "Invalid promoter_holding"})
        if row.get("pe_ratio", 0) < 0:
            failures.append({"rule_id": "DQ-05", "severity": "LOW", "issue": "Negative PE ratio"})
        if row.get("total_assets", 0) != row.get("total_liabilities", 0) + row.get("equity", 0):
            failures.append({"rule_id": "DQ-06", "severity": "HIGH", "issue": "Balance sheet mismatch"})
        if row.get("year", 0) < 2000 or row.get("year", 0) > 2030:
            failures.append({"rule_id": "DQ-07", "severity": "HIGH", "issue": "Out-of-range year"})
        if row.get("gross_margin", 0) < row.get("operating_margin", 0):
            failures.append({"rule_id": "DQ-08", "severity": "HIGH", "issue": "OPM > Gross Margin"})
        if row.get("cfo", 0) == 0 and row.get("revenue", 0) > 1000:
            failures.append({"rule_id": "DQ-09", "severity": "MEDIUM", "issue": "Zero CFO for high revenue"})
        if row.get("debt_to_equity", 0) > 20:
            failures.append({"rule_id": "DQ-10", "severity": "HIGH", "issue": "Extreme debt to equity"})
        if pd.isna(row.get("broad_sector")):
            failures.append({"rule_id": "DQ-11", "severity": "MEDIUM", "issue": "Missing sector"})
        if row.get("face_value", 0) <= 0:
            failures.append({"rule_id": "DQ-12", "severity": "LOW", "issue": "Invalid face value"})
        if row.get("audit_status") not in ["Audited", "Un-Audited"]:
            failures.append({"rule_id": "DQ-13", "severity": "HIGH", "issue": "Invalid audit status"})
        if row.get("tax_rate_pct", 0) > 50:
            failures.append({"rule_id": "DQ-14", "severity": "MEDIUM", "issue": "Tax rate over 50%"})
            
    return failures

# Base valid record generator
def get_valid_record():
    return {
        "company_id": "COMP_001", "revenue": 1000, "operating_margin": 20,
        "promoter_holding": 50, "pe_ratio": 15, "total_assets": 1000,
        "total_liabilities": 600, "equity": 400, "year": 2024,
        "gross_margin": 30, "cfo": 200, "debt_to_equity": 0.5,
        "broad_sector": "IT", "face_value": 10, "audit_status": "Audited",
        "tax_rate_pct": 25
    }

def test_rule_dq01_missing_company_id():
    rec = get_valid_record(); rec["company_id"] = None
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-01" for r in res)

def test_rule_dq02_negative_revenue():
    rec = get_valid_record(); rec["revenue"] = -100
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-02" for r in res)

def test_rule_dq03_invalid_margin():
    rec = get_valid_record(); rec["operating_margin"] = 150
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-03" for r in res)

def test_rule_dq04_invalid_promoter_holding():
    rec = get_valid_record(); rec["promoter_holding"] = 110
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-04" for r in res)

def test_rule_dq05_negative_pe():
    rec = get_valid_record(); rec["pe_ratio"] = -5
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-05" for r in res)

def test_rule_dq06_balance_sheet_mismatch():
    rec = get_valid_record(); rec["total_assets"] = 2000
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-06" for r in res)

def test_rule_dq07_out_of_range_year():
    rec = get_valid_record(); rec["year"] = 1995
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-07" for r in res)

def test_rule_dq08_opm_greater_than_gross_margin():
    rec = get_valid_record(); rec["gross_margin"] = 10; rec["operating_margin"] = 20
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-08" for r in res)

def test_rule_dq09_zero_cfo_high_revenue():
    rec = get_valid_record(); rec["cfo"] = 0; rec["revenue"] = 5000
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-09" for r in res)

def test_rule_dq10_extreme_de():
    rec = get_valid_record(); rec["debt_to_equity"] = 25
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-10" for r in res)

def test_rule_dq11_missing_sector():
    rec = get_valid_record(); rec["broad_sector"] = None
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-11" for r in res)

def test_rule_dq12_invalid_face_value():
    rec = get_valid_record(); rec["face_value"] = 0
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-12" for r in res)

def test_rule_dq13_invalid_audit_status():
    rec = get_valid_record(); rec["audit_status"] = "Unknown"
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-13" for r in res)

def test_rule_dq14_high_tax_rate():
    rec = get_valid_record(); rec["tax_rate_pct"] = 60
    res = apply_dq_rules(pd.DataFrame([rec]))
    assert any(r["rule_id"] == "DQ-14" for r in res)