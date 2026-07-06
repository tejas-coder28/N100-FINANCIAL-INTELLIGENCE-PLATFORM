import os
import pandas as pd
from openpyxl.styles import PatternFill

def generate_peer_comparison_report(data_df: pd.DataFrame, peer_groups_path="data/peer_groups.xlsx", output_path="output/peer_comparison.xlsx"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if not os.path.exists(peer_groups_path):
        return
        
    peer_df = pd.read_excel(peer_groups_path)
    merged_df = pd.merge(data_df, peer_df[['company_id', 'peer_group_name']], on='company_id', how='inner')
    
    metrics = ['roe', 'roce', 'npm', 'debt_to_equity', 'fcf', 'pat_cagr_5yr', 'revenue_cagr_5yr', 'eps_cagr_5yr', 'interest_coverage', 'asset_turnover']
    
    for m in metrics:
        if m in merged_df.columns:
            merged_df[m] = pd.to_numeric(merged_df[m], errors='coerce')
            
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for group_name, group_df in merged_df.groupby('peer_group_name'):
            sheet_df = group_df.copy()
            
            for m in metrics:
                if m in sheet_df.columns:
                    valid_s = sheet_df[m].dropna()
                    if len(valid_s) <= 1:
                        sheet_df[f'{m}_pct'] = 100.0
                    else:
                        if m == 'debt_to_equity':
                            sheet_df[f'{m}_pct'] = (1.0 - valid_s.rank(pct=True)) * 100.0
                        else:
                            sheet_df[f'{m}_pct'] = valid_s.rank(pct=True) * 100.0
            
            base_cols = ['company_id', 'company_name']
            metric_cols = []
            for m in metrics:
                if m in sheet_df.columns:
                    metric_cols.extend([m, f'{m}_pct'])
                    
            final_cols = [c for c in base_cols + metric_cols if c in sheet_df.columns]
            export_df = sheet_df[final_cols].copy()
            
            median_row = {'company_id': 'MEDIAN', 'company_name': 'Peer Group Median'}
            for m in metrics:
                if m in sheet_df.columns:
                    median_row[m] = sheet_df[m].median()
                    median_row[f'{m}_pct'] = ''
                    
            export_df = pd.concat([export_df, pd.DataFrame([median_row])], ignore_index=True)
            export_df.to_excel(writer, sheet_name=str(group_name)[:31], index=False)
            
            workbook = writer.book
            worksheet = workbook[str(group_name)[:31]]
            
            green = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
            yellow = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
            red = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
            gold = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
            
            cols = [str(cell.value).strip() for cell in worksheet[1]]
            max_r = worksheet.max_row
            
            for r_idx in range(2, max_r):
                cid_val = str(worksheet.cell(row=r_idx, column=1).value).strip()
                if "benchmark" in cid_val.lower() or r_idx == 2:
                    for c_idx in range(1, len(cols) + 1):
                        worksheet.cell(row=r_idx, column=c_idx).fill = gold
                        
                for m in metrics:
                    pct_col_name = f'{m}_pct'
                    if pct_col_name in cols:
                        c_idx = cols.index(pct_col_name) + 1
                        cell = worksheet.cell(row=r_idx, column=c_idx)
                        try:
                            val = float(cell.value)
                            if val >= 75.0:
                                cell.fill = green
                            elif val <= 25.0:
                                cell.fill = red
                            else:
                                cell.fill = yellow
                        except (ValueError, TypeError):
                            pass