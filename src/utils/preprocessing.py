import pandas as pd

def normalize_column_names(column_names: pd.Index) -> pd.Index:
    return column_names.str.replace(r'\s+', '_', regex=True).str.lower()

def normalize_datetimes(dates: pd.Series) -> pd.Series:
    return pd.to_datetime(dates, format='%m/%d/%y %H:%M:%S', errors='coerce')

def calc_trip_duration(df:pd.DataFrame, start_col_name:str, end_col_name:str, index:pd.Index=slice(None)):
    start_time = pd.to_datetime(df.loc[index, start_col_name])
    end_time = pd.to_datetime(df.loc[index, end_col_name])
    return (end_time - start_time).dt.total_seconds().astype('int64')
