# 🇲🇾 Bursa Malaysia Stock Data Downloader

📈 **Automate Bursa Malaysia (KLSE) stock data collection with ease**

---

## 🧭 Overview

This **Python script** automates the process of downloading **historical stock price data** for companies listed on **Bursa Malaysia (Kuala Lumpur Stock Exchange)** using the [`yfinance`](https://pypi.org/project/yfinance/) library.

It is designed to:

* ✅ Read a list of **4-digit stock codes** from a local file (`stock_codes.txt`)
* 🔧 Format these codes for Yahoo Finance (by appending `.KL`)
* 💾 Download **Adjusted Close** and **Close** prices only
* 📊 Export all results into a **single clean CSV file** for analysis

---

## 🚀 Getting Started

### 🧩 Prerequisites

Make sure you have **Python 3.8+** installed, then install the dependencies:

```bash
pip install yfinance pandas
```

---

### 📄 Step 1: Prepare Your Stock Code List

Create a text file named **`stock_codes.txt`** in the same directory as your script.
Each line should contain one **4-digit stock code** (without `.KL`).

**Example:**

```
7231
0271
5246
0008
```

---

### 🏃 Step 2: Run the Script

Run the Python script in your terminal or IDE:

```bash
python bursa_data_pipeline.py
```

---

## 📂 Output

When complete, the script generates a file named:

```
bursa_closing_prices_filtered.csv
```

This file contains daily historical data, with headers formatted as:

| Date | Adj Close,7231.KL | Close,7231.KL | Adj Close,0271.KL | Close,0271.KL | ... |
| ---- | ----------------- | ------------- | ----------------- | ------------- | --- |

---

## ⚙️ Configuration

You can easily modify the **date range** and **output settings** in the main script:

```python
if __name__ == "__main__":
    # Define date range (default: last 180 days)
    TODAY = datetime.now().strftime('%Y-%m-%d')
    START_DATE = (datetime.now() - pd.DateOffset(days=180)).strftime('%Y-%m-%d')

    # Output file name
    OUTPUT_FILE = 'bursa_closing_prices_filtered.csv'

    # Input ticker file
    TICKER_FILE_NAME = 'stock_codes.txt'
```

---

## 💡 Example Use Case

This script is useful for:

* 🧠 Academic or personal **financial analysis**
* 📊 Backtesting trading strategies
* 💼 Data collection for **machine learning models**

---

## 🛠️ Tech Stack

* **Python**
* **yfinance**
* **pandas**

---

## 🤝 Contributing

Pull requests are welcome!
If you'd like to improve the script, please open an issue or submit a PR.

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).

---

