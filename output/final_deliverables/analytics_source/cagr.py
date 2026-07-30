def compute_cagr(start_val: float, end_val: float, periods: int) -> tuple:
    if periods <= 0 or start_val is None or end_val is None:
        return None, "INSUFFICIENT"

    if start_val == 0:
        return None, "ZERO_BASE"

    if start_val > 0 and end_val < 0:
        return None, "DECLINE_TO_LOSS"

    if start_val < 0 and end_val > 0:
        return None, "TURNAROUND"

    if start_val < 0 and end_val < 0:
        return None, "BOTH_NEGATIVE"
        
    if (start_val < 0 and end_val == 0) or (start_val == 0 and end_val == 0):
        return None, "BOTH_NEGATIVE"

    try:
        ratio = end_val / start_val
        if ratio <= 0:
            return None, "BOTH_NEGATIVE"
            
        cagr_val = ((ratio) ** (1 / periods) - 1) * 100
        return round(cagr_val, 2), "NORMAL"
    except Exception:
        return None, "INSUFFICIENT"