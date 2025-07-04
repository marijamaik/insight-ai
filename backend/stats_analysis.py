# # Add these analysis functions:
# - descriptive_statistics()
# - correlation_analysis() 
# - outlier_detection()
# - trend_analysis()
# - data_quality_scoring()

import pandas as pd
import numpy as np

def descriptive_statistics(df: pd.DataFrame) -> dict:
    return df.describe(include='all').to_dict()

def correlation_analysis(df: pd.DataFrame) -> dict:
    numeric_df = df.select_dtypes(include=[np.number])
    return numeric_df.corr().to_dict()

def outlier_detection(df: pd.DataFrame, z_thresh: float = 3.0) -> dict:
    outliers = {}
    for col in df.select_dtypes(include=[np.number]):
        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
        outliers[col] = int((z_scores > z_thresh).sum())
    return outliers

def trend_analysis(df: pd.DataFrame, time_col: str = None) -> dict:
    if time_col and time_col in df.columns:
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
        df = df.dropna(subset=[time_col])
        df['month'] = df[time_col].dt.to_period('M')
        return df.groupby('month').size().to_dict()
    return {}

def data_quality_scoring(df: pd.DataFrame) -> float:
    total = df.size
    missing = df.isnull().sum().sum()
    score = 100 - (missing / total * 100)
    return round(score, 2)
