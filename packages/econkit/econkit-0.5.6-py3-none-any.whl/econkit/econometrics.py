import warnings
import inspect
import pandas as pd
import numpy as np
from scipy.stats import kurtosis, skew, jarque_bera, spearmanr, pearsonr, kendalltau, shapiro, kstest
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.stattools import durbin_watson
from tabulate import tabulate



 
def descriptives(data):
	"""
	Computes descriptive statistics for each numeric column in a DataFrame.

	Parameters:
	data: pandas.DataFrame
		The DataFrame from which the statistics will be calculated.

	Returns:
	None
		Prints a summary table of the descriptive statistics for each numeric column in the DataFrame.
	"""
	statistics_labels = [
		"Mean", "Median", "Min", "Max", "St. Deviation",
		"Quartile Deviation", "Kurtosis Fisher", "Kurtosis Pearson",
		"Skewness", "Co-efficient of Q.D", "Q1 (25%)", "Q3 (75%)",
		"Jarque-Bera", "p-value"
	]
	descriptive_df = pd.DataFrame({'STATISTICS': statistics_labels})

	for name in data.columns:
		if pd.api.types.is_numeric_dtype(data[name]):
			column_data = data[name].dropna()

			jb_test = jarque_bera(column_data)
			jb_value = jb_test[0]
			p_value = jb_test[1]

			statistics_values = [
				format(
					column_data.mean(), '.3f')[
					1:] if column_data.mean() < 1 else format(
					column_data.mean(), '.3f'),
				format(
					column_data.median(), '.3f')[
					1:] if column_data.median() < 1 else format(
					column_data.median(), '.3f'),
				format(
					column_data.min(), '.3f')[
					1:] if column_data.min() < 1 else format(
					column_data.min(), '.3f'),
				format(
					column_data.max(), '.3f')[
					1:] if column_data.max() < 1 else format(
					column_data.max(), '.3f'),
				format(
					column_data.std(), '.3f')[
					1:] if column_data.std() < 1 else format(
					column_data.std(), '.3f'),
				format((np.percentile(column_data,
									  75) - np.percentile(column_data,
														  25)) / 2,
					   '.3f')[1:] if (np.percentile(column_data,
													75) - np.percentile(column_data,
																		25)) / 2 < 1 else format((np.percentile(column_data,
																												75) - np.percentile(column_data,
																																	25)) / 2,
																								 '.3f'),
				format(
					kurtosis(
						column_data,
						fisher=True,
						nan_policy='omit'),
					'.3f')[
					1:] if kurtosis(
					column_data,
					fisher=True,
					nan_policy='omit') < 1 else format(
					kurtosis(
						column_data,
						fisher=True,
						nan_policy='omit'),
					'.3f'),
				format(
					kurtosis(
						column_data,
						fisher=False,
						nan_policy='omit'),
					'.3f')[
					1:] if kurtosis(
					column_data,
					fisher=False,
					nan_policy='omit') < 1 else format(
					kurtosis(
						column_data,
						fisher=False,
						nan_policy='omit'),
					'.3f'),
				format(
					column_data.skew(), '.3f')[
					1:] if column_data.skew() < 1 else format(
					column_data.skew(), '.3f'),
				format((np.percentile(column_data,
									  75) - np.percentile(column_data,
														  25)) / 2 / column_data.median(),
					   '.3f')[1:] if column_data.median() != 0 and (np.percentile(column_data,
																				  75) - np.percentile(column_data,
																									  25)) / 2 / column_data.median() < 1 else format((np.percentile(column_data,
																																									 75) - np.percentile(column_data,
																																														 25)) / 2 / column_data.median(),
																																					  '.3f') if column_data.median() != 0 else '0.000',
				format(
					np.percentile(
						column_data,
						25),
					'.3f')[
					1:] if np.percentile(
					column_data,
					25) < 1 else format(
					np.percentile(
						column_data,
						25),
					'.3f'),
				# Q1
				format(
					np.percentile(
						column_data,
						75),
					'.3f')[
					1:] if np.percentile(
					column_data,
					75) < 1 else format(
					np.percentile(
						column_data,
						75),
					'.3f'),
				# Q3
				format(
					jb_value, '.3f')[
					1:] if jb_value < 1 else format(
					jb_value, '.3f'),
				format(
					p_value, '.3f')[
					1:] if p_value < 1 else format(
					p_value, '.3f')
			]

			descriptive_df[name] = statistics_values

	print("=" *
		  (len("Descriptive Statistics") +
		   2) +
		  "\n" +
		  " Descriptive Statistics" +
		  "\n" +
		  "=" *
		  (len("Descriptive Statistics") +
		   2) +
		  "\n")
	print(
		tabulate(
			descriptive_df,
			headers='keys',
			tablefmt='pretty',
			showindex=False))

 
def correlation(df, method="Pearson", pvalue=False):
	"""
	Calculates and prints the correlation matrix and p-values for numeric columns
	in the provided DataFrame. Supports Pearson, Spearman, and Kendall correlation methods.

	Parameters:
	df: pandas.DataFrame
		The DataFrame for which correlations are calculated.
	method: str, optional
		The method of correlation ('Pearson', 'Spearman', or 'Kendall'). Default is 'Pearson'.
	pvalue: bool, optional
		If True, p-value matrix is also printed; if False, only correlation matrix
		is printed. Default is False.

	Returns:
	None
		This function prints the correlation matrix and optionally the p-value
		matrix directly to the console.
	"""

	numeric_df = df.select_dtypes(include=[np.number])
	if method == "Pearson":
		print("=" * 21 + f"\n {method} Correlation\n" + "=" * 21)
	elif method == "Spearman":
		print("=" * 27 + f"\n {method} Rank Correlation\n" + "=" * 27)
	elif method == "Kendall":
		print("=" * 25 + f"\n {method} Tau Correlation\n" + "=" * 25)

	corr_matrix = pd.DataFrame(
		index=numeric_df.columns,
		columns=numeric_df.columns)
	pmatrix = pd.DataFrame(
		index=numeric_df.columns,
		columns=numeric_df.columns)

	keys = numeric_df.columns.tolist()

	for i, key1 in enumerate(keys):
		for j, key2 in enumerate(keys):
			if i > j:
				continue

			data1 = numeric_df[key1].dropna()
			data2 = numeric_df[key2].dropna()

			common_index = data1.index.intersection(data2.index)
			data1 = data1.loc[common_index]
			data2 = data2.loc[common_index]

			if len(common_index) < 2:
				corr_matrix.at[key1, key2] = 'nan'
				corr_matrix.at[key2, key1] = 'nan'
				pmatrix.at[key1, key2] = 'nan'
				pmatrix.at[key2, key1] = 'nan'
				continue

			if method == 'Spearman':
				correlation, p_value = spearmanr(data1, data2)
			elif method == 'Pearson':
				correlation, p_value = pearsonr(data1, data2)
			elif method == 'Kendall':
				correlation, p_value = kendalltau(data1, data2)

			p_value_str = format(
				p_value, '.3f')[
				1:] if p_value < 1 else format(
				p_value, '.3f')

			if i == j:  # If it's the diagonal element
				p_value_str = ""

			pmatrix.at[key1, key2] = p_value_str
			pmatrix.at[key2, key1] = p_value_str

			stars = "     "
			if p_value < 0.001:
				stars = " *** "
			elif p_value < 0.01:
				stars = " **  "
			elif p_value < 0.05:
				stars = " *   "
			elif p_value < 0.1:
				stars = " .   "

			correlation_str = f"{format(correlation, '.3f')[1:] if correlation < 1 else format(correlation, '.2f')}{stars}"

			if i == j:  # If it's the diagonal element
				correlation_str = ""

			corr_matrix.at[key1, key2] = correlation_str
			corr_matrix.at[key2, key1] = correlation_str

	corr_matrix_str = tabulate(
		corr_matrix, headers='keys', tablefmt='pretty')

	print("\n\n>> Correlation Matrix <<\n")
	print(corr_matrix_str)
	print("\n--\nSignif. codes:  0.001 '***', 0.01 '**', 0.05 '*', 0.1 '.'")

	if pvalue:
		pmatrix_str = tabulate(pmatrix, headers='keys', tablefmt='pretty')
		print("\n\n>> P-Value Matrix <<\n")
		print(pmatrix_str)
		print("\n")
	else:
		print("\n")

 
def adf(
		dataframe,
		maxlag=None,
		regression='c',
		autolag='AIC',
		handle_na='drop'):
	"""
	Perform Augmented Dickey-Fuller (ADF) test on each column in the DataFrame and return a summary table.

	Parameters:
	dataframe: pandas.DataFrame or pandas.Series
		The DataFrame or Series containing time series data to be tested.
	maxlag: int, optional
		Maximum number of lags to use. Default is None, which means the lag length is automatically determined.
	regression: str {'c', 'ct', 'ctt', 'nc'}, optional
		Type of regression trend. Default is 'c' for constant only.
		'c' : constant only (default)
		'ct' : constant and trend
		'ctt' : constant, and linear and quadratic trend
		'nc' : no constant, no trend
	autolag: str, optional
		Method to use when automatically determining the lag length among 'AIC', 'BIC', 't-stat'. Default is 'AIC'.
	handle_na: str {'drop', 'fill'}, optional
		How to handle missing values:
		'drop' : drop missing values (default)
		'fill' : fill missing values forward and then backward

	Returns:
	None
		Prints a summary table of the ADF test results for each column in the DataFrame.

	The summary table includes:
	- ADF Statistic
	- Significance codes
	- P-value
	- Number of lags used
	- Number of observations
	- Information Criterion
	- Critical values at 1%, 5%, and 10%
	"""
	def adf_test(series):
		# Handle NaN and infinite values
		if handle_na == 'drop':
			series = series.dropna()
		elif handle_na == 'fill':
			series = series.fillna(method='ffill').fillna(method='bfill')

		# Ensure no infinite values
		series = series[np.isfinite(series)]

		if series.size == 0:
			return {
				'ADF Stat.': 'nan',
				'P-Value': 'nan',
				'Number of Lags Used': 'nan',
				'Number of Observations': 'nan',
				'Information Criterion': 'nan',
				'critical value 1%': 'nan',
				'critical value 5%': 'nan',
				'critical value 10%': 'nan'
			}

		try:
			result = adfuller(
				series,
				maxlag=maxlag,
				regression=regression,
				autolag=autolag)
		except Exception as e:
			print(f"ADF test failed for series: {series.name}, error: {e}")
			return {
				'ADF Stat.': 'nan',
				'P-Value': 'nan',
				'Number of Lags Used': 'nan',
				'Number of Observations': 'nan',
				'Information Criterion': 'nan',
				'critical value 1%': 'nan',
				'critical value 5%': 'nan',
				'critical value 10%': 'nan'
			}

		adf_stat = format(
			result[0], '.3f')[
			1:] if result[0] < 1 else format(
			result[0], '.3f'),
		p_value = format(
			result[1], '.3f')[
			1:] if result[1] < 1 else format(
			result[1], '.3f'),
		used_lag = result[2]
		n_obs = result[3]
		critical_values = result[4]
		ic_best = (format(result[5], '.3f')[1:] if result[5] < 1 else format(
			result[5], '.3f')) if autolag is not None else None

		# Determine significance codes
		stars = ""
		if p_value < 0.001:
			stars = " ***"
		elif p_value < 0.01:
			stars = " **"
		elif p_value < 0.05:
			stars = " *"
		elif p_value < 0.1:
			stars = " ."

		summary = {
			'ADF Stat.': f"{adf_stat:.3f}{stars}",
			'P-Value': f"{p_value:.3f}",
			'Number of Lags Used': used_lag,
			'Number of Observations': n_obs,
			'Information Criterion': ic_best
		}

		# Adding critical values to the summary
		for key, value in critical_values.items():
			summary[f'critical value {key}'] = round(value, 3)

		return summary

	if isinstance(dataframe, pd.Series):
		# If the input is a Series, convert it to a DataFrame with one
		# column
		dataframe = dataframe.to_frame(name=dataframe.name)

	# Apply the ADF test to each column in the DataFrame
	adf_results = dataframe.apply(adf_test)

	# Transform the results into a DataFrame with the desired structure
	result_dict = {
		series_name: results for series_name,
		results in adf_results.items()}

	# Create the result DataFrame
	results_df = pd.DataFrame(result_dict)

	print("=" *
		  (len("Augmented Dickey-Fuller Test") +
		   2) +
		  "\n" +
		  " Augmented Dickey-Fuller Test" +
		  "\n" +
		  "=" *
		  (len("Augmented Dickey-Fuller Test") +
		   2) +
		  "\n")
	print(
		tabulate(
			results_df,
			headers='keys',
			tablefmt='pretty',
			showindex=True))
	print(
		"\n--\n" +
		"Signif. codes:  0.001 '***', 0.01 '**', 0.05 '*', 0.1 '.'\n")

 
def kpss(dataframe, regression='c', nlags='auto', handle_na='drop'):
	"""
	Perform Kwiatkowski-Phillips-Schmidt-Shin test on each column in the DataFrame and return a summary table.

	Parameters:
	dataframe: pandas.DataFrame or pandas.Series
		The DataFrame or Series containing time series data to be tested.
	regression: str {'c', 'ct'}, optional
		Type of regression trend. Default is 'c' for constant only.
		'c' : constant only (default)
		'ct' : constant and trend
	nlags: str or int, optional
		Number of lags to use. Default is 'auto' which uses automatic lag selection.
	handle_na: str {'drop', 'fill'}, optional
		How to handle missing values:
		'drop' : drop missing values (default)
		'fill' : fill missing values forward and then backward

	Returns:
	None
		Prints a summary table of the KPSS test results for each column in the DataFrame.

	The summary table includes:
	- KPSS Statistic
	- Significance codes
	- P-value
	- Number of lags used
	- Critical values at 1%, 5%, and 10%
	"""
	def kpss_test(series):
		# Handle NaN values
		if handle_na == 'drop':
			series = series.dropna()
		elif handle_na == 'fill':
			series = series.fillna(method='ffill').fillna(method='bfill')

		# Ensure no infinite values
		series = series[np.isfinite(series)]

		if series.size == 0:
			return {
				'KPSS Stat.': 'nan',
				'P-Value': 'nan',
				'Number of Lags Used': 'nan',
				'critical value 1%': 'nan',
				'critical value 5%': 'nan',
				'critical value 10%': 'nan'
			}

		try:
			with warnings.catch_warnings(record=True) as w:
				warnings.simplefilter("always")
				result = kpss(series, regression=regression, nlags=nlags)
				p_value = result[1]
				if any("InterpolationWarning" in str(warn.message)
					   for warn in w):
					p_value = '> {}'.format(p_value)
		except Exception as e:
			print(
				f"KPSS test failed for series: {series.name}, error: {e}")
			return {
				'KPSS Stat.': 'nan',
				'P-Value': 'nan',
				'Number of Lags Used': 'nan',
				'critical value 1%': 'nan',
				'critical value 5%': 'nan',
				'critical value 10%': 'nan'
			}

		kpss_stat = round(result[0], 3)
		lags_used = result[2]
		critical_values = result[3]

		# Determine significance codes
		stars = "     "
		if p_value < 0.001:
			stars = " ***"
		elif p_value < 0.01:
			stars = " **"
		elif p_value < 0.05:
			stars = " *"
		elif p_value < 0.1:
			stars = " ."

		summary = {
			'KPSS Stat.': f"{kpss_stat:.3f}{stars}",
			'P-Value': f"{p_value:.3f}",
			'Number of Lags Used': lags_used,
			'critical value 1%': round(critical_values['1%'], 3),
			'critical value 5%': round(critical_values['5%'], 3),
			'critical value 10%': round(critical_values['10%'], 3)
		}

		return summary

	if isinstance(dataframe, pd.Series):
		# If the input is a Series, convert it to a DataFrame with one
		# column
		dataframe = dataframe.to_frame()

	# Apply the KPSS test to each column in the DataFrame
	kpss_results = dataframe.apply(kpss_test).T

	# Transform the results into a DataFrame with the desired structure
	result_dict = {
		series_name: results for series_name,
		results in kpss_results.items()}

	# Create the result DataFrame
	results_df = pd.DataFrame(result_dict)

	print("=" *
		  (len("Kwiatkowski-Phillips-Schmidt-Shin Test") +
		   2) +
		  "\n" +
		  " Kwiatkowski-Phillips-Schmidt-Shin Test" +
		  "\n" +
		  "=" *
		  (len("Kwiatkowski-Phillips-Schmidt-Shin Test") +
		   2) +
		  "\n")
	print(
		tabulate(
			results_df,
			headers='keys',
			tablefmt='pretty',
			showindex=True))
	print(
		"\n--\n" +
		"Signif. codes:  0.001 '***', 0.01 '**', 0.05 '*', 0.1 '.'\n")

 
def dw(data):
	"""
	Perform Durbin-Watson autocorrelation test and Ljung-Box test for each column of the dataset.

	Parameters:
	data (pd.DataFrame): A pandas DataFrame where each column is a time series.

	Returns:
	pd.DataFrame: A DataFrame containing the Durbin-Watson statistic and p-values for each column.
	"""
	results = []

	for column in data.columns:
		time_series = data[column].dropna()
		if len(
				time_series) > 1:  # Ensure there are enough data points for regression
			# Add constant term for intercept
			X = sm.add_constant(range(len(time_series)))
			model = sm.OLS(time_series, X).fit()
			dw_statistic = durbin_watson(model.resid)
			lb_test = acorr_ljungbox(model.resid, lags=[1], return_df=True)
			p_value = lb_test['lb_pvalue'].iloc[0]
			results.append(
				(column, format(
					dw_statistic, '.3f'), format(
					p_value, '.3f')[
					1:] if p_value < 1 else format(
					p_value, '.3f')))
		else:
			# Not enough data points for regression
			results.append((column, None, None))

	results_df = pd.DataFrame(results, columns=[' ', ' Stat.', 'P-Value'])
	results_df = results_df.set_index(' ')

	print("=" *
		  (len("Durbin-Watson Test") +
		   2) +
		  "\n" +
		  " Durbin-Watson Test" +
		  "\n" +
		  "=" *
		  (len("Durbin-Watson Test") +
		   2) +
		  "\n\n")
	print(results_df.to_string(index=True))

 
def normality_tests(data, pvalue=False):
	"""
	Perform normality tests (Shapiro-Wilk, Kolmogorov-Smirnov)
	on each column of a DataFrame and display results as a formatted table.

	Parameters:
		data (pd.DataFrame): A DataFrame containing numerical data.
		pvalue (bool): If True, p-value matrix is also printed; if False, only test results are printed. Default is False.

	Returns:
		None: Prints formatted test results and optionally p-value matrix.
	"""
	numeric_df = data.select_dtypes(include=[np.number])
	print("=" * 17 + "\n Normality Tests \n" + "=" * 17)

	results_matrix = pd.DataFrame(
		index=numeric_df.columns, columns=[
			"Shapiro-Wilk", "Kolmogorov-Smirnov"])
	pmatrix = pd.DataFrame(
		index=numeric_df.columns, columns=[
			"Shapiro-Wilk", "Kolmogorov-Smirnov"])

	for column in numeric_df.columns:
		col_data = numeric_df[column].dropna()

		if col_data.empty:
			results_matrix.loc[column] = ["nan", "nan"]
			pmatrix.loc[column] = ["nan", "nan"]
			continue

		# Shapiro-Wilk Test
		shapiro_stat, shapiro_p = shapiro(col_data)
		shapiro_signif = significance_code(shapiro_p)
		results_matrix.at[column,
						  "Shapiro-Wilk"] = f"{shapiro_stat:.3f}{shapiro_signif}"
		pmatrix.at[column, "Shapiro-Wilk"] = f"{shapiro_p:.3f}"

		# Kolmogorov-Smirnov Test
		ks_stat, ks_p = kstest(
			col_data, 'norm', args=(
				np.mean(col_data), np.std(col_data)))
		ks_signif = significance_code(ks_p)
		results_matrix.at[column,
						  "Kolmogorov-Smirnov"] = f"{ks_stat:.3f}{ks_signif}"
		pmatrix.at[column, "Kolmogorov-Smirnov"] = f"{ks_p:.3f}"

	# Print formatted test results
	results_matrix_str = tabulate(
		results_matrix, headers='keys', tablefmt='pretty')
	print("\n\n>> Results Matrix <<\n")
	print(results_matrix_str)
	print("\n--\nSignif. codes:  0.001 '***', 0.01 '**', 0.05 '*', 0.1 '.'")

	# Optionally print p-value matrix
	if pvalue:
		pmatrix_str = tabulate(pmatrix, headers='keys', tablefmt='pretty')
		print("\n\n>> P-Value Matrix <<\n")
		print(pmatrix_str)
		print("\n")
	else:
		print("\n")

def significance_code(p_value):
	"""Assign significance codes based on p-value."""
	if p_value < 0.001:
		return "***"
	elif p_value < 0.01:
		return "**"
	elif p_value < 0.05:
		return "*"
	elif p_value < 0.1:
		return "."
	else:
		return ""

 
def random_number_generator(
		num_vars,
		num_random,
		distribution,
		mean=0,
		std_dev=1,
		seed=None,
		lower=None,
		upper=None,
		p=None,
		n_trials=None,
		lambda_param=None,
		start=None,
		stop=None,
		step=None,
		repeat_each=None,
		repeat_sequence=None):
	"""
	Generates random numbers based on the specified distribution and parameters.

	Parameters:
		num_vars (int): Number of variables (columns) of random numbers.
		num_random (int): Number of random numbers (rows) to generate per variable.
		distribution (str): The distribution to use ('normal', 'uniform', 'binomial', 'bernoulli', 'poisson', 'patterned').
		mean (float): Mean of the distribution (for normal). Default is 0.
		std_dev (float): Standard deviation of the distribution (for normal). Default is 1.
		lower (float): Lower bound for uniform distribution.
		upper (float): Upper bound for uniform distribution.
		p (float): Probability for Bernoulli or Binomial distribution.
		n_trials (int): Number of trials for Binomial distribution.
		lambda_param (float): Lambda for Poisson distribution.
		start (float): Start of range for patterned distribution.
		stop (float): Stop of range for patterned distribution.
		step (float): Step size for patterned distribution.
		repeat_each (int): Number of times to repeat each number in patterned distribution.
		repeat_sequence (int): Number of times to repeat the entire sequence in patterned distribution.
		seed (int): Random seed for reproducibility. Default is None.

	Returns:
		pandas.DataFrame: A DataFrame containing the generated random numbers.
	"""
	# Set random seed for reproducibility
	if seed is not None:
		np.random.seed(seed)

	# Initialize an empty dictionary to store data for each variable
	data = {}

	for i in range(num_vars):
		if distribution.lower() == 'normal' or distribution.lower(
		) == 'Normal' or distribution.lower() == 'NORMAL':
			if mean is None or std_dev is None:
				raise ValueError(
					"Mean and standard deviation must be provided for normal distribution.")
			data[f"Var{i+1}"] = np.random.normal(
				loc=mean, scale=std_dev, size=num_random)
		elif distribution.lower() == 'uniform' or distribution.lower() == 'Uniform' or distribution.lower() == 'UNIFORM':
			if lower is None or upper is None:
				raise ValueError(
					"Lower and upper bounds must be provided for uniform distribution.")
			data[f"Var{i+1}"] = np.random.uniform(lower, upper, num_random)
		elif distribution.lower() == 'binomial' or distribution.lower() == 'Binomial' or distribution.lower() == 'BINOMIAL':
			if p is None or n_trials is None:
				raise ValueError(
					"Probability and number of trials must be provided for binomial distribution.")
			data[f"Var{i+1}"] = np.random.binomial(
				n=n_trials, p=p, size=num_random)
		elif distribution.lower() == 'bernoulli' or distribution.lower() == 'Bernoulli' or distribution.lower() == 'BERNOULLI':
			if p is None:
				raise ValueError(
					"Probability must be provided for Bernoulli distribution.")
			if not (0 <= p <= 1):
				raise ValueError(
					"Probability for Bernoulli distribution must be between 0 and 1.")
			data[f"Var{i+1}"] = np.random.binomial(
				n=1, p=p, size=num_random)
		elif distribution.lower() == 'poisson' or distribution.lower() == 'Poisson' or distribution.lower() == 'POISSON':
			if lambda_param is None:
				raise ValueError(
					"Lambda parameter must be provided for Poisson distribution.")
			if lambda_param <= 0:
				raise ValueError(
					"Lambda (mean) for Poisson distribution must be greater than 0.")
			data[f"Var{i+1}"] = np.random.poisson(
				lam=lambda_param, size=num_random)
		elif distribution.lower() == 'patterned' or distribution.lower() == 'Patterned' or distribution.lower() == 'PATTERNED':
			if start is None or stop is None or step is None or repeat_each is None or repeat_sequence is None:
				raise ValueError(
					"Start, stop, step, repeat_each, and repeat_sequence must be provided for patterned distribution.")
			sequence = np.arange(start, stop, step)
			repeated_sequence = np.repeat(sequence, repeat_each)
			full_sequence = np.tile(
				repeated_sequence,
				repeat_sequence)[
				:num_random]
			data[f"Var{i+1}"] = full_sequence
		else:
			raise ValueError(
				"Unsupported distribution. Please use 'normal', 'uniform', 'binomial', 'bernoulli', 'poisson', or 'patterned'.")

	# Convert dictionary to DataFrame
	df = pd.DataFrame(data)

	return df

 
def combine_dataframes(column_name, *dataframes):
	"""
	Combine multiple dataframes based on a specified column into a new dataframe.

	Parameters:
	- dataframes: Multiple dataframes passed as positional arguments.
	- column_name (str): The column to extract from each dataframe.

	Returns:
	- pd.DataFrame: A new dataframe containing the specified column from each dataframe as separate columns, aligned by the Date index.
	"""
	combined_data = {}
	frame = inspect.currentframe().f_back
	for i, df in enumerate(dataframes):
		df_name = [
			name for name,
			obj in frame.f_locals.items() if obj is df][0]
		if column_name in df.columns:
			combined_data[df_name] = df[column_name]
		else:
			print(
				f"Warning: Column '{column_name}' not found in dataframe '{df_name}'.")

	# Combine dataframes by aligning on the Date index
	result = pd.concat(combined_data, axis=1)
	return result
