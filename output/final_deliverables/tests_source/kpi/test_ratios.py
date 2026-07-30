import pytest
import pandas as pd
import numpy as np

# Mock Ratio Calculator Functions
def calculate_roe(pat, equity):
    if equity <= 0:
        return None
    return (pat / equity) * 100

def calculate_de(total_debt, equity):
    if equity <= 0:
        return None
    if total_debt == 0:
        return 0.0
    return total_debt / equity

def calculate_icr(ebit, interest_expense):
    if interest_expense == 0:
        return None
    return ebit / interest_expense

def check_de_flag(de_ratio, broad_sector):
    if broad_sector != "Financial Services" and de_ratio > 5.0:
        return "HIGH_LEVERAGE_WARNING"
    return "NORMAL"

def calculate_cagr(start_val, end_val, periods):
    if start_val <= 0 or end_val <= 0:
        if start_val < 0 and end_val > 0:
            return "TURNAROUND"
        if start_val > 0 and end_val < 0:
            return "DECLINE_TO_LOSS"
        return None
    return ((end_val / start_val) ** (1 / periods) - 1) * 100

def check_opm_divergence(opm_pct, cfo, revenue):
    if revenue == 0:
        return False
    cfo_margin = (cfo / revenue) * 100
    return abs(opm_pct - cfo_margin) > 15.0

def calculate_cfo_quality_score(cfo, pat):
    if pat <= 0:
        return 0.0 if cfo <= 0 else 50.0
    ratio = cfo / pat
    if ratio >= 1.0:
        return 100.0
    elif ratio >= 0.7:
        return 75.0
    elif ratio >= 0.5:
        return 50.0
    return 25.0

# Unit Tests (20 Tests)
def test_roe_positive_equity():
    assert calculate_roe(150, 1000) == 15.0

def test_roe_zero_equity():
    assert calculate_roe(150, 0) is None

def test_roe_negative_equity():
    assert calculate_roe(150, -200) is None

def test_roe_loss_positive_equity():
    assert calculate_roe(-50, 1000) == -5.0

def test_de_normal_company():
    assert calculate_de(500, 1000) == 0.5

def test_de_debt_free():
    assert calculate_de(0, 1000) == 0.0

def test_de_negative_equity():
    assert calculate_de(500, -100) is None

def test_icr_normal():
    assert calculate_icr(500, 50) == 10.0

def test_icr_zero_interest():
    assert calculate_icr(500, 0) is None

def test_icr_loss_making():
    assert calculate_icr(-100, 50) == -2.0

def test_de_flag_non_financial_high():
    assert check_de_flag(5.5, "IT") == "HIGH_LEVERAGE_WARNING"

def test_de_flag_non_financial_normal():
    assert check_de_flag(2.0, "IT") == "NORMAL"

def test_de_flag_financial_high():
    assert check_de_flag(8.0, "Financial Services") == "NORMAL"

def test_cagr_standard_growth():
    cagr = calculate_cagr(100, 161.051, 5)
    assert abs(cagr - 10.0) < 0.01

def test_cagr_turnaround_flag():
    assert calculate_cagr(-50, 100, 5) == "TURNAROUND"

def test_cagr_decline_to_loss_flag():
    assert calculate_cagr(100, -20, 5) == "DECLINE_TO_LOSS"

def test_cagr_both_negative():
    assert calculate_cagr(-100, -50, 5) is None

def test_opm_divergence_detected():
    assert check_opm_divergence(25.0, 50, 1000) is True

def test_opm_divergence_not_detected():
    assert check_opm_divergence(20.0, 180, 1000) is False

def test_cfo_quality_score_excellent():
    assert calculate_cfo_quality_score(120, 100) == 100.0