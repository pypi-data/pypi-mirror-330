import os
import pandas as pd
import yfinance as yf
from datetime import datetime

def data(
		ticker_symbol: str,
		start_date: str,
		end_date: str,
		interval: str) -> pd.DataFrame:
	"""
	Downloads stock data for a given ticker symbol from Yahoo Finance, calculates daily returns,
	and saves the data to a CSV file.

	Args:
		ticker_symbol (str): The stock ticker symbol to fetch data for (e.g., 'AAPL' for Apple Inc.).
		start_date (str): The start date for the data in 'DD-MM-YYYY' format.
		end_date (str): The end date for the data in 'DD-MM-YYYY' format.
		interval (str): The data interval (e.g., '1d' for daily, '1wk' for weekly).

	Returns:
		pd.DataFrame: A pandas DataFrame containing the stock data with an additional column 'Returns',
					  which represents the percentage change in the 'Close' price.

	Notes:
		- Converts the input start_date and end_date from 'DD-MM-YYYY' to 'YYYY-MM-DD' format.
		- Creates a directory named 'Financial Data' if it does not exist.
		- Saves the downloaded data as a CSV file in the 'Financial Data' folder.
		- CSV file naming convention: '<ticker_symbol>_<interval>_<start_date>_<end_date>.csv'.

	Example:
		data('AAPL', '01-01-2024', '31-12-2024', '1d')
		- Downloads daily data for Apple Inc. from 01 January 2020 to 31 December 2020.
		- Saves the data to 'Financial Data/AAPL_1d_2020-01-01_2020-12-31.csv'.

	Raises:
		ValueError: If the input date format is incorrect or any issue arises in downloading data.
	"""

	def convert_date_format(date_string):
		"""
		Converts a date string from 'DD-MM-YYYY' to 'YYYY-MM-DD' format.

		Args:
			date_string (str): Date string in 'DD-MM-YYYY' format.

		Returns:
			str: Date string in 'YYYY-MM-DD' format.
		"""
		try:
			return datetime.strptime(
				date_string, '%d-%m-%Y').strftime('%Y-%m-%d')
		except ValueError as e:
			raise ValueError(
				f"Invalid date format: {date_string}. Expected 'DD-MM-YYYY'.") from e

	# Convert dates to the required format
	start_date = convert_date_format(start_date)
	end_date = convert_date_format(end_date)

	# Download stock data
	try:
		stock_data = yf.download(
			ticker_symbol,
			start=start_date,
			end=end_date,
			interval=interval,
			auto_adjust=False,
			prepost=True)
	except Exception as e:
		raise ValueError(
			f"Error downloading data for {ticker_symbol}: {e}")

	# Calculate percentage change in the 'Close' price
	stock_data['%C'] = stock_data['Close'].pct_change()
	
	stock_data.columns = stock_data.columns.droplevel(1)

	# Create directory if it doesn't exist
	folder_name = "Financial Data"
	if not os.path.exists(folder_name):
		os.makedirs(folder_name)

	# Save the data to a CSV file
	file_name = f"{folder_name}/{ticker_symbol}_{interval}_{start_date}_{end_date}.csv"
	stock_data.to_csv(file_name)

	return stock_data
