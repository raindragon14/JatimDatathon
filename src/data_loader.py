"""
Utility functions for data loading and preprocessing for the Jatim Datathon project.
This module abstracts the basic pandas operations to maintain clean notebooks.
"""

import pandas as pd
from typing import Optional
import os

def load_csv_data(filepath: str, encoding: str = 'utf-8') -> Optional[pd.DataFrame]:
    """
    Safely loads a CSV file into a Pandas DataFrame.
    
    Args:
        filepath (str): The relative or absolute path to the dataset.
        encoding (str): The file encoding, defaults to 'utf-8'.
        
    Returns:
        Optional[pd.DataFrame]: The loaded dataframe, or None if an error occurs.
    """
    if not os.path.exists(filepath):
        print(f"Error: The file {filepath} was not found.")
        return None
        
    try:
        df = pd.read_csv(filepath, encoding=encoding)
        print(f"Successfully loaded {filepath} with shape {df.shape}")
        return df
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        return None

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names by converting them to lowercase and replacing spaces with underscores.
    
    Args:
        df (pd.DataFrame): The input dataframe.
        
    Returns:
        pd.DataFrame: A new dataframe with cleaned column names.
    """
    df_clean = df.copy()
    df_clean.columns = [str(col).strip().lower().replace(' ', '_') for col in df_clean.columns]
    return df_clean
