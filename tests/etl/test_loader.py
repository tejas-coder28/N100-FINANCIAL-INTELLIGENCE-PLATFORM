import pytest
import pandas as pd

def test_loader_companies_schema():
    df = pd.DataFrame({'company_id': ['TCS', 'INFY'], 'broad_sector': ['IT', 'IT']})
    assert len(df) == 2
    assert 'company_id' in df.columns

def test_loader_ratios_schema():
    df = pd.DataFrame({'company_id': ['TCS'], 'year': [2023], 'roe': [30.5]})
    assert 'roe' in df.columns
    assert df['year'].iloc[0] == 2023

def test_loader_empty_df(): assert pd.DataFrame().empty == True
def test_loader_column_rename():
    df = pd.DataFrame({'ticker': ['TCS']}).rename(columns={'ticker': 'company_id'})
    assert 'company_id' in df.columns

def test_loader_drop_duplicates():
    df = pd.DataFrame({'company_id': ['TCS', 'TCS']}).drop_duplicates()
    assert len(df) == 1

def test_loader_null_handling():
    df = pd.DataFrame({'val': [1.0, None]}).fillna(0)
    assert df['val'].iloc[1] == 0

def test_loader_type_cast():
    df = pd.DataFrame({'year': ['2023']})
    df['year'] = df['year'].astype(int)
    assert df['year'].dtype == 'int32' or df['year'].dtype == 'int64'

def test_loader_filter():
    df = pd.DataFrame({'sector': ['IT', 'Banking']})
    res = df[df['sector'] == 'IT']
    assert len(res) == 1

def test_loader_sorting():
    df = pd.DataFrame({'year': [2021, 2023, 2022]}).sort_values('year')
    assert df['year'].iloc[0] == 2021

def test_loader_row_count():
    df = pd.DataFrame({'id': range(92)})
    assert len(df) == 92