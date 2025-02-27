import os
import pandas as pd
import yfinance as yf
from datetime import datetime

def data(ticker_symbol: str, start_date: str, end_date: str, interval: str) -> pd.DataFrame:
    """
    Downloads stock data for a given ticker symbol from Yahoo Finance, calculates daily returns,
    and saves the data to a CSV file.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL').
        start_date (str): The start date in 'DD-MM-YYYY' format.
        end_date (str): The end date in 'DD-MM-YYYY' format.
        interval (str): The data interval (e.g., '1d' for daily).

    Returns:
        pd.DataFrame: The downloaded stock data with an additional 'Returns' column.
    """
    def convert_date_format(date_string):
        try:
            return datetime.strptime(date_string, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError as e:
            raise ValueError(f"Invalid date format: {date_string}. Expected 'DD-MM-YYYY'.") from e

    # Convert dates to the required format.
    start_date = convert_date_format(start_date)
    end_date = convert_date_format(end_date)

    # Download stock data.
    try:
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval=interval)
    except Exception as e:
        raise ValueError(f"Error downloading data for {ticker_symbol}: {e}")

    # Filter out any rows where 'Close' cannot be converted to numeric values.
    stock_data = stock_data[pd.to_numeric(stock_data['Close'], errors='coerce').notnull()]

    # Calculate percentage change in the 'Close' price.
    stock_data['Returns'] = stock_data['Close'].pct_change()

    # Create directory if it does not exist.
    folder_name = "Financial Data"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Save the data to a CSV file.
    file_name = f"{folder_name}/{ticker_symbol}_{interval}_{start_date}_{end_date}.csv"
    stock_data.to_csv(file_name)

    return stock_data
