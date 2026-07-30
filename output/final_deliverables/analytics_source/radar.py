import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_company_radar_charts(data_df: pd.DataFrame, peer_groups_path="data/peer_groups.xlsx", output_dir="reports/radar_charts/"):
    os.makedirs(output_dir, exist_ok=True)
    
    if os.path.exists(peer_groups_path):
        try:
            peer_df = pd.read_excel(peer_groups_path)
            merged_df = pd.merge(data_df, peer_df[['company_id', 'peer_group_name']], on='company_id', how='left')
        except Exception:
            merged_df = data_df.copy()
            merged_df['peer_group_name'] = np.nan
    else:
        merged_df = data_df.copy()
        merged_df['peer_group_name'] = np.nan

    metrics = ['roe', 'roce', 'npm', 'debt_to_equity', 'fcf', 'pat_cagr_5yr', 'revenue_cagr_5yr', 'composite_quality_score']
    labels = ['ROE', 'ROCE', 'NPM', 'D/E', 'FCF Score', 'PAT CAGR 5Y', 'Rev CAGR 5Y', 'Composite']
    num_vars = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    def parse_series(df_in):
        for m in metrics:
            df_in[m] = pd.to_numeric(df_in[m], errors='coerce').fillna(0.0)
        return df_in

    merged_df = parse_series(merged_df)
    nifty_avg = merged_df[metrics].mean().to_numpy().tolist()
    nifty_avg += nifty_avg[:1]

    for idx, row in merged_df.iterrows():
        cid = row['company_id']
        group_name = row['peer_group_name']
        
        c_values = row[metrics].to_numpy().tolist()
        c_values += c_values[:1]
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        
        if pd.isna(group_name) or str(group_name).strip() == '':
            ax.plot(angles, nifty_avg, color='gray', linewidth=1.5, linestyle='--', label='Nifty 100 Avg')
            title_suffix = "(vs Nifty 100)"
        else:
            group_df = merged_df[merged_df['peer_group_name'] == group_name]
            peer_avg = group_df[metrics].mean().to_numpy().tolist()
            peer_avg += peer_avg[:1]
            ax.plot(angles, peer_avg, color='red', linewidth=1.5, linestyle='--', label=f'{group_name} Avg')
            title_suffix = f"(vs {group_name})"
            
        ax.plot(angles, c_values, color='teal', linewidth=2, linestyle='solid', label=str(cid))
        ax.fill(angles, c_values, color='teal', alpha=0.25)
        
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=9)
        
        plt.title(f"{cid} Performance Radar {title_suffix}", size=11, y=1.1, weight='bold')
        plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=8)
        
        out_path = os.path.join(output_dir, f"{cid}_radar.png")
        plt.savefig(out_path, bbox_inches='tight', dpi=150)
        plt.close(fig)