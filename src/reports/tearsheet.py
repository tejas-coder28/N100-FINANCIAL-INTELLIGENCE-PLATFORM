import os
import sqlite3
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

DB_PATH = "data/financial_analytics.db"
OUTPUT_DIR = "output/reports"

def generate_pdf_tearsheet(company_id: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_filename = os.path.join(OUTPUT_DIR, f"{company_id}_tearsheet.pdf")
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=12
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1E40AF'),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = styles['Normal']

    story = []

    # Title Banner
    story.append(Paragraph(f"Executive Financial Tearsheet: {company_id}", title_style))
    story.append(Spacer(1, 10))

    # Fetch Data from SQLite
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        try:
            df_intel = pd.read_sql_query(f"SELECT * FROM analytics_cashflow_intelligence WHERE company_id = '{company_id}'", conn)
        except Exception:
            df_intel = pd.DataFrame()
        conn.close()
    else:
        df_intel = pd.DataFrame()

    # Section 1: Key Summary Metrics Table
    story.append(Paragraph("Key Financial Metrics", section_heading))
    
    if not df_intel.empty:
        latest_row = df_intel.iloc[-1]
        table_data = [
            ["Metric", "Value"],
            ["Company ID", str(latest_row.get("company_id", company_id))],
            ["Capital Pattern", str(latest_row.get("sprint2_capital_pattern", "N/A"))],
            ["FCF Score", str(latest_row.get("fcf_score", "N/A"))],
            ["Distress Risk Level", str(latest_row.get("distress_level", "Normal"))]
        ]
    else:
        table_data = [
            ["Metric", "Value"],
            ["Company ID", company_id],
            ["Status", "No recorded DB data found"]
        ]

    t = Table(table_data, colWidths=[200, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3F4F6')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # Section 2: Analyst Notes & Disclaimer
    story.append(Paragraph("Analyst Summary", section_heading))
    story.append(Paragraph(
        f"This automated tearsheet compiles quantitative risk indicators, capital deployment metrics, "
        f"and cash flow intelligence for {company_id}. Generated via N100 Financial Intelligence Engine.",
        body_style
    ))

    doc.build(story)
    print(f"Generated PDF report: {pdf_filename}")

if __name__ == "__main__":
    generate_pdf_tearsheet("COMP_001")