import os
import yaml
import numpy as np
import pandas as pd
from scipy.stats import mstats

def load_screener_config(config_path="config/screener_config.yaml"):
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config.get("filters", {})

def apply_threshold_filters(df: pd.DataFrame, custom_filters: dict = None) -> pd.DataFrame:
    filtered_df = df.copy()
    active_filters = custom_filters if custom_filters is not None else load_screener_config()
    
    def parse_numeric(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return np.nan

    numeric_metrics = [
        'roe', 'roce', 'npm', 'fcf', 'fcf_cagr_15%','cfo_pat_ratio', 'revenue_cagr_5yr', 
        'pat_cagr_5yr', 'opm', 'pe', 'pb', 'dividend_yield', 'market_cap', 
        'net_profit', 'eps_cagr', 'asset_turnover', 'sales', 'revenue_cagr_10%', 
        'pat_cagr_10%', 'revenue_cagr_3yr', 'de_current', 'de_previous', 'dividend_payout', 'revenue'
    ]
    for metric in numeric_metrics:
        if metric in filtered_df.columns:
            filtered_df[metric] = filtered_df[metric].apply(parse_numeric)

    if 'debt_to_equity' in filtered_df.columns:
        filtered_df['debt_to_equity'] = filtered_df['debt_to_equity'].apply(parse_numeric)

    if 'interest_coverage_ratio' in filtered_df.columns:
        def clean_icr(val):
            if isinstance(val, str) and "debt free" in val.strip().lower():
                return np.inf
            return parse_numeric(val)
        filtered_df['interest_coverage_ratio'] = filtered_df['interest_coverage_ratio'].apply(clean_icr)

    if 'roe_min' in active_filters and 'roe' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['roe'] >= active_filters['roe_min']]
        
    if 'de_max' in active_filters and 'debt_to_equity' in filtered_df.columns:
        is_financial = filtered_df['broad_sector'].astype(str).str.strip().str.lower() == 'financials'
        passes_de = filtered_df['debt_to_equity'] <= active_filters['de_max']
        filtered_df = filtered_df[is_financial | passes_de]

    if 'fcf_min' in active_filters and 'fcf' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['fcf'] >= active_filters['fcf_min']]

    if 'revenue_cagr_5yr_min' in active_filters and 'revenue_cagr_5yr' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['revenue_cagr_5yr'] >= active_filters['revenue_cagr_5yr_min']]

    if 'pat_cagr_5yr_min' in active_filters and 'pat_cagr_5yr' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['pat_cagr_5yr'] >= active_filters['pat_cagr_5yr_min']]

    if 'opm_min' in active_filters and 'opm' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['opm'] >= active_filters['opm_min']]

    if 'pe_max' in active_filters and 'pe' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['pe'] <= active_filters['pe_max']]

    if 'pb_max' in active_filters and 'pb' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['pb'] <= active_filters['pb_max']]

    if 'dividend_yield_min' in active_filters and 'dividend_yield' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['dividend_yield'] >= active_filters['dividend_yield_min']]

    if 'icr_min' in active_filters and 'interest_coverage_ratio' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['interest_coverage_ratio'] >= active_filters['icr_min']]

    if 'market_cap_min' in active_filters and 'market_cap' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['market_cap'] >= active_filters['market_cap_min']]

    if 'net_profit_min' in active_filters and 'net_profit' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['net_profit'] >= active_filters['net_profit_min']]

    if 'eps_cagr_min' in active_filters and 'eps_cagr' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['eps_cagr'] >= active_filters['eps_cagr_min']]

    if 'asset_turnover_min' in active_filters and 'asset_turnover' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['asset_turnover'] >= active_filters['asset_turnover_min']]

    if 'sales_min' in active_filters and 'sales' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['sales'] >= active_filters['sales_min']]

    return filtered_df

def compute_composite_quality_score(df: pd.DataFrame) -> pd.DataFrame:
    res_df = df.copy()
    metrics = [
        'roe', 'roce', 'npm', 'fcf_cagr_15%', 'cfo_pat_ratio', 
        'revenue_cagr_10%', 'pat_cagr_10%', 'debt_to_equity', 'interest_coverage_ratio'
    ]
    
    for m in metrics:
        if m not in res_df.columns:
            res_df[m] = 0.0
        res_df[m] = pd.to_numeric(res_df[m], errors='coerce').fillna(0.0)
        if m == 'interest_coverage_ratio':
            res_df[m] = res_df[m].replace(np.inf, 99999.0)

    def winsorize_and_scale(series, invert=False):
        arr = series.to_numpy()
        if len(arr) > 1:
            arr = mstats.winsorize(arr, limits=[0.1, 0.1])
        amin, amax = np.min(arr), np.max(arr)
        if amax == amin:
            return pd.Series(50.0, index=series.index)
        scaled = ((arr - amin) / (amax - amin)) * 100.0
        if invert:
            scaled = 100.0 - scaled
        return pd.Series(scaled, index=series.index)

    for m in metrics:
        invert_flag = True if m == 'debt_to_equity' else False
        res_df[f'{m}_score'] = res_df.groupby('broad_sector')[m].transform(lambda x: winsorize_and_scale(x, invert=invert_flag))

    fcf_pos = res_df['fcf'].apply(lambda x: 100.0 if x > 0 else 0.0)
    
    prof = 0.15 * res_df['roe_score'] + 0.10 * res_df['roce_score'] + 0.10 * res_df['npm_score']
    cash = 0.15 * res_df['fcf_cagr_15%_score'] + 0.10 * res_df['cfo_pat_ratio_score'] + 0.05 * fcf_pos
    growth = 0.10 * res_df['revenue_cagr_10%_score'] + 0.10 * res_df['pat_cagr_10%_score']
    leverage = 0.10 * res_df['debt_to_equity_score'] + 0.05 * res_df['interest_coverage_ratio_score']
    
    res_df['composite_quality_score'] = prof + cash + growth + leverage
    return res_df.sort_values(by='composite_quality_score', ascending=False)

def run_quality_compounder(df: pd.DataFrame) -> pd.DataFrame:
    custom = {'roe_min': 15.0, 'de_max': 1.0, 'fcf_min': 0.0, 'revenue_cagr_5yr_min': 10.0}
    return compute_composite_quality_score(apply_threshold_filters(df, custom))

def run_value_pick(df: pd.DataFrame) -> pd.DataFrame:
    custom = {'pe_max': 20.0, 'pb_max': 3.0, 'de_max': 2.0, 'dividend_yield_min': 1.0}
    return compute_composite_quality_score(apply_threshold_filters(df, custom))

def run_growth_accelerator(df: pd.DataFrame) -> pd.DataFrame:
    custom = {'pat_cagr_5yr_min': 20.0, 'revenue_cagr_5yr_min': 15.0, 'de_max': 2.0}
    return compute_composite_quality_score(apply_threshold_filters(df, custom))

def run_dividend_champion(df: pd.DataFrame) -> pd.DataFrame:
    custom = {'dividend_yield_min': 2.0, 'fcf_min': 0.0}
    filtered = apply_threshold_filters(df, custom)
    if 'dividend_payout' in filtered.columns:
        filtered = filtered[pd.to_numeric(filtered['dividend_payout'], errors='coerce').fillna(0.0) < 80.0]
    return compute_composite_quality_score(filtered)

def run_debt_free_blue_chip(df: pd.DataFrame) -> pd.DataFrame:
    custom = {'de_max': 0.0, 'roe_min': 12.0}
    filtered = apply_threshold_filters(df, custom)
    if 'revenue' in filtered.columns:
        filtered = filtered[pd.to_numeric(filtered['revenue'], errors='coerce').fillna(0.0) > 5000.0]
    return compute_composite_quality_score(filtered)

def run_turnaround_watch(df: pd.DataFrame) -> pd.DataFrame:
    custom = {'fcf_min': 0.0}
    filtered = apply_threshold_filters(df, custom)
    if 'revenue_cagr_3yr' in filtered.columns:
        filtered = filtered[pd.to_numeric(filtered['revenue_cagr_3yr'], errors='coerce').fillna(0.0) > 10.0]
    if 'de_current' in filtered.columns and 'de_previous' in filtered.columns:
        filtered = filtered[pd.to_numeric(filtered['de_current'], errors='coerce').fillna(0.0) < pd.to_numeric(filtered['de_previous'], errors='coerce').fillna(0.0)]
    return compute_composite_quality_score(filtered)

def export_screener_output(universe_df: pd.DataFrame, output_path="output/screener_output.xlsx"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    presets = {
        "Quality Compounder": (run_quality_compounder, {'roe': 15.0, 'debt_to_equity': 1.0, 'fcf': 0.0, 'revenue_cagr_5yr': 10.0}),
        "Value Pick": (run_value_pick, {'pe': 20.0, 'pb': 3.0, 'debt_to_equity': 2.0, 'dividend_yield': 1.0}),
        "Growth Accelerator": (run_growth_accelerator, {'pat_cagr_5yr': 20.0, 'revenue_cagr_5yr': 15.0, 'debt_to_equity': 2.0}),
        "Dividend Champion": (run_dividend_champion, {'dividend_yield': 2.0, 'dividend_payout': 80.0, 'fcf': 0.0}),
        "Debt-Free Blue Chip": (run_debt_free_blue_chip, {'debt_to_equity': 0.0, 'roe': 12.0, 'revenue': 5000.0}),
        "Turnaround Watch": (run_turnaround_watch, {'revenue_cagr_3yr': 10.0, 'fcf': 0.0})
    }
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, (run_func, thresholds) in presets.items():
            out_df = run_func(universe_df)
            out_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            workbook = writer.book
            worksheet = workbook[sheet_name]
            
            from openpyxl.styles import PatternFill
            green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
            red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
            
            cols = [str(cell.value).strip().lower() for cell in worksheet[1]]
            
            for row_idx in range(2, worksheet.max_row + 1):
                sector_val = ""
                if 'broad_sector' in cols:
                    sector_val = str(worksheet.cell(row=row_idx, column=cols.index('broad_sector') + 1).value).strip().lower()
                
                for metric_name, t_val in thresholds.items():
                    if metric_name in cols:
                        col_idx = cols.index(metric_name) + 1
                        cell = worksheet.cell(row=row_idx, column=col_idx)
                        try:
                            c_val = float(cell.value)
                        except (ValueError, TypeError):
                            continue
                            
                        if metric_name == 'debt_to_equity' and sector_val == 'financials':
                            cell.fill = green_fill
                            continue
                            
                        if metric_name in ['pe', 'pb', 'dividend_payout']:
                            cell.fill = green_fill if c_val <= t_val else red_fill
                        elif metric_name == 'debt_to_equity':
                            cell.fill = green_fill if c_val <= t_val else red_fill
                        elif metric_name == 'turnaround_watch' and metric_name in ['de_current', 'de_previous']:
                            pass
                        else:
                            cell.fill = green_fill if c_val >= t_val else red_fill