# ----------------------------------------------------------------------
# Bursa Malaysia Stock Data Pipeline
# ----------------------------------------------------------------------

import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# IMPORTANT: Ensure you have the required libraries installed:
# pip install yfinance pandas

# Define the filename where your stock codes are stored (one code per line)
TICKER_FILE_NAME = 'stock_codes.txt'

def read_tickers_from_file(filename):
    """
    Reads stock codes from a text file, handling cleanup.
    
    Args:
        filename (str): The path to the text file containing one stock code per line.
        
    Returns:
        list: A list of clean, 4-digit stock codes.
    """
    print(f"Attempting to read stock codes from: {filename}")
    raw_codes = []
    try:
        with open(filename, 'r') as f:
            # Read all lines, strip whitespace (like the newline character '\n'),
            # and filter out any empty lines.
            raw_codes = [line.strip() for line in f if line.strip()]
        
        print(f"Successfully read {len(raw_codes)} raw codes.")
        return raw_codes
        
    except FileNotFoundError:
        print(f"ERROR: Ticker file '{filename}' not found.")
        print("Please ensure the file is in the same directory as the script.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while reading the ticker file: {e}")
        return []


def get_bursa_tickers():
    """
    Retrieves stock codes either from the dedicated file or falls back
    to a small hardcoded list if the file is missing or empty.
    
    Returns:
        list: A list of full YFinance-compatible tickers (e.g., ['7231.KL', '0271.KL']).
    """
    # Attempt to read codes from the dedicated file
    raw_codes = read_tickers_from_file(TICKER_FILE_NAME)
    
    # if not raw_codes:
    #     print(f"Falling back to hardcoded example list as '{TICKER_FILE_NAME}' was empty or not found.")
    #     # Fallback list (the original hardcoded list)
    #     raw_codes = [
    #         '7231', '0271', '0298', '5246', '5009', '0162', '0008', '6378',
    #         '7050', '7025', '4243', '5156', '5267', '7043', '7121', '0165',
    #         '0140', '0017', '7003'
    #     ]
    
    # Apply the required '.KL' suffix for Bursa Malaysia stocks on yfinance
    bursa_tickers = [code + '.KL' for code in raw_codes]
    return bursa_tickers


def export_stock_data_filtered(tickers, start_date, end_date, output_filename):
    """
    Fetches historical stock data (Adj Close and Close only) and exports it,
    handling both single-ticker and multi-ticker DataFrame structures and 
    safely filtering for existing columns.
    """
    REQUIRED_COLUMNS = ['Adj Close', 'Close']
    
    if not tickers:
        print("Skipping download: Tickers list is empty.")
        return

    print(f"--- Starting data download for {len(tickers)} Bursa Malaysia tickers ---")
    print(f"Date Range: {start_date} to {end_date}")

    try:
        # 1. Fetch data
        data = yf.download(
            tickers=tickers,
            start=start_date,
            end=end_date,
            interval="1d",
            progress=True
        )

        if data.empty:
            print("Warning: No data was returned. Check if the market was open during this range or if tickers are correct.")
            return

        # 2. ROBUST FLEXIBLE FILTERING: Select only the 'Adj Close' and 'Close' columns
        
        if isinstance(data.columns, pd.MultiIndex):
            # Case 1: Multiple tickers were successfully downloaded (MultiIndex)
            # Find which of the REQUIRED_COLUMNS are actually present at the top level
            available_cols = [col for col in REQUIRED_COLUMNS if col in data.columns.get_level_values(0)]
            
            if not available_cols:
                print("Error: None of the required columns ('Adj Close', 'Close') were found in the downloaded data.")
                print(f"Available top-level columns: {data.columns.get_level_values(0).unique().tolist()}")
                return

            print(f"Detected MultiIndex (Multiple Tickers). Filtering for available columns: {available_cols}")
            # Use data[available_cols] which returns a DataFrame with a MultiIndex structure
            data_filtered = data[available_cols]

        elif all(col in data.columns for col in REQUIRED_COLUMNS):
            # Case 2: Only one ticker was successfully downloaded (Simple Index) and both columns exist
            print("Detected Simple Index (Single Ticker). Filtering by column names.")
            data_filtered = data[REQUIRED_COLUMNS]
        
        elif any(col in data.columns for col in REQUIRED_COLUMNS):
            # Case 3: Only one ticker downloaded, and only one of the required columns exists
            available_cols = [col for col in REQUIRED_COLUMNS if col in data.columns]
            print(f"Detected Simple Index (Single Ticker) but only partial data. Filtering for: {available_cols}")
            data_filtered = data[available_cols]
            
        else:
            # Case 4: Error or unexpected structure
            print("Error: Could not find any of the required columns in the downloaded data.")
            print(f"Available columns: {data.columns.tolist()}")
            return

        print("\n--- Data successfully downloaded and filtered ---")
        print(f"Filtered Data Shape: {data_filtered.shape}")

        # 3. Export the filtered Pandas DataFrame to a CSV file
        data_filtered.to_csv(output_filename)

        print(f"\n✅ Success! Filtered data saved to '{output_filename}'")
        print(f"File Location: {os.path.abspath(output_filename)}")

    except Exception as e:
        print(f"\nAn error occurred during download or export: {e}")
        print("Ensure all tickers are valid and yfinance is not experiencing temporary issues.")


if __name__ == "__main__":
    # --- Configuration ---
    
    # Get the list of tickers prepared for yfinance
    STOCK_TICKERS = get_bursa_tickers()

    # Define the desired date range
    TODAY = datetime.now().strftime('%Y-%m-%d')
    # Fetching the last 180 days of data
    START_DATE = (datetime.now() - pd.DateOffset(days=180)).strftime('%Y-%m-%d')
    
    OUTPUT_FILE = 'bursa_closing_prices_filtered.csv'

    # Execute the data fetching and export process
    export_stock_data_filtered(
        tickers=STOCK_TICKERS,
        start_date=START_DATE,
        end_date=TODAY,
        output_filename=OUTPUT_FILE
    )
