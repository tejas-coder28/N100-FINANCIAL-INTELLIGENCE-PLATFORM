import pytest
import re

def normalize_year(val):
    if val is None:
        return None
    val_str = str(val).strip()
    if not val_str or val_str == "0":
        return None
        
    # Check for 4-digit years first (e.g., 2023, FY2021, 2020/21, 31/03/2022)
    match_4digit = re.search(r'\b(19\d{2}|20\d{2})\b', val_str)
    if match_4digit:
        return int(match_4digit.group(1))
        
    # Check for 2-digit short year formats (e.g., FY24, Mar-23, FY-25)
    match_2digit = re.search(r'(?:FY|Mar|CY|Jan|Feb|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-\s]?(\d{2})\b', val_str, re.IGNORECASE)
    if match_2digit:
        yr = int(match_2digit.group(1))
        return 2000 + yr if yr < 50 else 1900 + yr

    # Fallback digit extraction
    digits = "".join([c for c in val_str if c.isdigit()])
    if len(digits) == 4:
        yr = int(digits)
        return yr if 1900 <= yr <= 2100 else None

    return None

def test_norm_standard_year(): assert normalize_year(2023) == 2023
def test_norm_string_year(): assert normalize_year("2022") == 2022
def test_norm_fy_format(): assert normalize_year("FY2021") == 2021
def test_norm_slash_format(): assert normalize_year("2020/21") == 2020
def test_norm_hyphen_format(): assert normalize_year("2019-2020") == 2019
def test_norm_none(): assert normalize_year(None) == None
def test_norm_empty(): assert normalize_year("") == None
def test_norm_float(): assert normalize_year(2024.0) == 2024
def test_norm_short_digits(): assert normalize_year("99") == None
def test_norm_out_of_range(): assert normalize_year("1850") == None
def test_norm_future_out_of_range(): assert normalize_year("2200") == None
def test_norm_with_spaces(): assert normalize_year("  2018  ") == 2018
def test_norm_date_str(): assert normalize_year("2023-03-31") == 2023
def test_norm_cy_format(): assert normalize_year("CY2022") == 2022
def test_norm_mar_format(): assert normalize_year("Mar-23") == 2023
def test_norm_full_date_slash(): assert normalize_year("31/03/2022") == 2022
def test_norm_invalid_text(): assert normalize_year("invalid") == None
def test_norm_zero(): assert normalize_year(0) == None
def test_norm_fy_short(): assert normalize_year("FY24") == 2024
def test_norm_fy_hyphen(): assert normalize_year("FY-2025") == 2025