import re

def normalize_ticker(ticker: str) -> str:
    if not ticker:
        return ""
    cleaned = str(ticker).strip().upper()
    cleaned = re.sub(r'\.(NS|BSE)$', '', cleaned)
    return cleaned

def normalize_year(year_val) -> int:
    if year_val is None:
        return 0
    str_val = str(year_val).strip()
    digits = re.findall(r'\d+', str_val)
    if not digits:
        return 0
    val = int(digits[0])
    if val < 100:
        return 2000 + val if val > 50 else 1900 + val
    return val