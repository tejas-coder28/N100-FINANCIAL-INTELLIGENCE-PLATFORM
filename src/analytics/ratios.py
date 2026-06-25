import logging

def compute_net_profit_margin(net_profit, sales):
    if sales == 0: return None
    return (net_profit / sales) * 100

def compute_operating_profit_margin(op, sales, source_opm_pct=None, company_id=None):
    if sales == 0: return None
    calc = (op / sales) * 100
    if source_opm_pct is not None and abs(calc - source_opm_pct) > 0.01:
        logging.info(f"OPM Mismatch for {company_id}")
    return calc

def compute_return_on_equity(net_income, equity, pref_dividends=0):
    if equity <= 0: return None
    return ((net_income - pref_dividends) / equity) * 100

def compute_roce(ebit, total_assets, current_liabilities, min_capital=0, broad_sector=None, company_id=None):
    if broad_sector == "Financials":
        logging.info(f"Financials sector detected for {company_id}")
    capital = total_assets - current_liabilities
    if capital <= min_capital: return None
    return (ebit / capital) * 100

def compute_return_on_assets(net_income, total_assets):
    if total_assets <= 0: return None
    return (net_income / total_assets) * 100

def compute_debt_to_equity(total_debt, equity, total_assets, broad_sector=None):
    if equity <= 0: return None, False
    ratio = total_debt / equity
    flag = ratio > 5.0 if broad_sector != "Financials" else False
    return ratio, flag

def compute_interest_coverage_ratio(ebit, interest_expense, total_debt):
    if total_debt == 0 or interest_expense == 0:
        return None, "Debt Free", False
    ratio = ebit / interest_expense
    return ratio, "Normal", (ratio < 1.5)

def compute_asset_turnover(sales, total_assets):
    if total_assets <= 0: return None
    return sales / total_assets