import pandas as pd

def normalize_columns(columns: pd.Index) -> pd.Index:
    return columns.str.replace(r'\s+', '_', regex=True).str.lower()
