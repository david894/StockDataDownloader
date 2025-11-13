## Bursa Malaysia Stock Data Downloader 

📈 Project Overview

This Python script is designed to automate the process of downloading historical stock price data for companies listed on Bursa Malaysia (Kuala Lumpur Stock Exchange) using the yfinance library.

It is specifically configured to:

1. Read a list of 4-digit stock codes from a local file (stock_codes.txt).

Format these codes for Yahoo Finance compatibility (by adding the .KL suffix).

Download only the Adjusted Close and Close prices to ensure cleaner data for analysis.

Export the consolidated data into a single CSV file.



🚀 Getting Started

Prerequisites

You need Python installed. Then, install the required libraries:

pip install yfinance pandas


1. Prepare Your Ticker File

Create a plain text file named stock_codes.txt in the same directory as the script. This file should contain one 4-digit stock code per line, followed by a newline (Enter).

Example of stock_codes.txt:

7231
0271
5246
0008
... (all your codes)


2. Run the Script

Execute the main Python script:

python bursa_data_pipeline.py



📂 Output

Upon successful execution, the script will generate a file named bursa_closing_prices_filtered.csv in the same directory.

The CSV file will contain the daily historical data, with headers structured to show the metric (Adj Close or Close) and the stock ticker (e.g., Adj Close, 7231.KL).

⚙️ Configuration

You can easily adjust the date range and output file name within the if __name__ == "__main__": block of the bursa_data_pipeline.py file:

if __name__ == "__main__":
    # ...
    # Define the desired date range (currently set to the last 180 days)
    TODAY = datetime.now().strftime('%Y-%m-%d')
    START_DATE = (datetime.now() - pd.DateOffset(days=180)).strftime('%Y-%m-%d')
    
    OUTPUT_FILE = 'bursa_closing_prices_filtered.csv'

    # The file the script reads from
    TICKER_FILE_NAME = 'stock_codes.txt'
    # ...
