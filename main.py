"""
Main entry point for the Jatim Datathon project.
Demonstrates how to utilize the utility functions from the `src` directory 
to load and clean datasets consistently across the project.
"""

import os
from src.data_loader import load_csv_data, clean_column_names

def main() -> None:
    print("🚀 Starting Jatim Datathon Data Pipeline...\n")
    
    # Example: Loading a raw dataset
    # We will pick one of the known files in data/raw to demonstrate
    sample_file_path = os.path.join('data', 'raw', 'data_upah_minimum_provinsi_ump.csv')
    
    print(f"Attempting to load: {sample_file_path}")
    df = load_csv_data(sample_file_path)
    
    if df is not None:
        print("\nOriginal Data Preview:")
        print(df.head(2))
        
        # Clean the column names
        df_clean = clean_column_names(df)
        print("\nCleaned Columns Preview:")
        print(df_clean.columns.tolist())
        
        print("\n✅ Data loading module is working perfectly!")
    else:
        print(f"\n⚠️ Could not find '{sample_file_path}'. Please ensure the data directory is populated.")

if __name__ == "__main__":
    main()
