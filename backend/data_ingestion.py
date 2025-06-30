import pandas as pd

# This module provides functions for cleaning and profiling dataframes
def clean_and_profile(df: pd.DataFrame) -> dict:
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df.drop_duplicates(inplace=True)

    profile = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": []
    }

    for col in df.columns:
        dtype = str(df[col].dtype)
        missing = df[col].isnull().sum()
        unique = df[col].nunique()
        profile["columns"].append({
            "name": col,
            "dtype": dtype,
            "missing": int(missing),
            "unique": int(unique)
        })
    
    return profile
