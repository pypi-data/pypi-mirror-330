# EconKit - Function Descriptions

`econkit` is a Python library that provides various statistical and econometric analysis tools, including descriptive statistics, correlation matrices, and tests for stationarity and autocorrelation.

## Functions

---

### Descriptive Statistics

#### `descriptives(data)`
Computes descriptive statistics for each numeric column in a DataFrame.

**Parameters:**
- `data`: `pandas.DataFrame` containing the data to be analyzed.

**Returns:**
- None. Prints a summary table of the descriptive statistics.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics as ec

df = pd.read_csv('your_data.csv')
ec.descriptives(df)
```

---

### Correlation Matrix

#### `correlation(df, method='Pearson', p=False)`
Calculates and prints the correlation matrix and p-values for numeric columns in the provided DataFrame. Supports Pearson, Spearman, and Kendall correlation methods.

**Parameters:**
- `df`: `pandas.DataFrame` containing the data to be analyzed.
- `method`: `str` (optional). Method of correlation ('Pearson', 'Spearman', or 'Kendall'). Default is 'Pearson'.
- `p`: `bool` (optional). If True, p-value matrix is also printed; if False, only the correlation matrix is printed.

**Returns:**
- None. Prints the correlation matrix and optionally the p-value matrix.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics as ec

df = pd.read_csv('your_data.csv')
ec.correlation(df, method='Spearman', p=True)
```

---

### Augmented Dickey-Fuller (ADF) Test

#### `adf(dataframe, maxlag=None, regression='c', autolag='AIC', handle_na='drop')`
Performs the ADF test on each column in the DataFrame and returns a summary table.

**Parameters:**
- `dataframe`: `pandas.DataFrame` containing the data to be tested.
- `maxlag`: `int` (optional). Maximum number of lags to use.
- `regression`: `str` (optional). Type of regression trend ('c', 'ct', 'ctt', 'nc'). Default is 'c'.
- `autolag`: `str` (optional). Method for lag length selection ('AIC', 'BIC', 't-stat').
- `handle_na`: `str` (optional). How to handle missing values ('drop' or 'fill').

**Returns:**
- None. Prints a summary table of the ADF test results.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics as ec

df = pd.read_csv('your_data.csv')
ec.adf(df)
```

---

### KPSS Test

#### `kpss(dataframe, regression='c', nlags='auto', handle_na='drop')`
Performs the KPSS test on each column in the DataFrame and returns a summary table.

**Parameters:**
- `dataframe`: `pandas.DataFrame` containing the data to be tested.
- `regression`: `str` (optional). Type of regression trend ('c' or 'ct'). Default is 'c'.
- `nlags`: `str` or `int` (optional). Number of lags to use. Default is 'auto'.
- `handle_na`: `str` (optional). How to handle missing values ('drop' or 'fill').

**Returns:**
- None. Prints a summary table of the KPSS test results.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics as ec

df = pd.read_csv('your_data.csv')
ec.kpss(df)
```

---

### Durbin-Watson Test

#### `dw(data)`
Performs the Durbin-Watson autocorrelation test and Ljung-Box test for each column of the dataset.

**Parameters:**
- `data`: `pandas.DataFrame` containing the time series data.

**Returns:**
- None. Prints a summary table of the Durbin-Watson test results.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics as ec

df = pd.read_csv('your_data.csv')
ec.dw(df)
```

---

### Normality Tests

#### `normality_tests(data, pvalue=False)`
Performs normality tests (Shapiro-Wilk and Kolmogorov-Smirnov) on each column of a DataFrame and displays results as a formatted table.

**Parameters:**
- `data`: `pandas.DataFrame` containing the numerical data.
- `pvalue`: `bool` (optional). If True, displays the p-value matrix along with the test results. Default is False.

**Returns:**
- None. Prints the results matrix and optionally the p-value matrix.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics as ec

df = pd.read_csv('your_data.csv')
ec.normality_tests(df, pvalue=True)
```

---

### Random Number Generator

#### `random_number_generator(num_vars, num_random, distribution, mean=0, std_dev=1, seed=None, lower=None, upper=None, p=None, n_trials=None, lambda_param=None, start=None, stop=None, step=None, repeat_each=None, repeat_sequence=None)`
Generates random numbers based on the specified distribution and parameters.

**Parameters:**
- `num_vars`: `int`. Number of variables (columns) to generate.
- `num_random`: `int`. Number of random values per variable.
- `distribution`: `str`. The distribution type ('normal', 'uniform', 'binomial', 'bernoulli', 'poisson', 'patterned').
- `mean`: `float`. Mean for the normal distribution. Default is 0.
- `std_dev`: `float`. Standard deviation for the normal distribution. Default is 1.
- `lower`: `float`. Lower bound for the uniform distribution.
- `upper`: `float`. Upper bound for the uniform distribution.
- `p`: `float`. Probability for Bernoulli or Binomial distributions.
- `n_trials`: `int`. Number of trials for the Binomial distribution.
- `lambda_param`: `float`. Lambda parameter for the Poisson distribution.
- `start`: `float`. Start value for the patterned distribution.
- `stop`: `float`. Stop value for the patterned distribution.
- `step`: `float`. Step size for the patterned distribution.
- `repeat_each`: `int`. Number of times to repeat each number in the patterned distribution.
- `repeat_sequence`: `int`. Number of times to repeat the entire sequence.

**Returns:**
- `pandas.DataFrame`. A DataFrame containing the generated random numbers.

**Example Usage:**
```python
from econkit import econometrics as ec

random_data = ec.random_number_generator(num_vars=2, num_random=10, distribution='normal', mean=0, std_dev=1, seed=42)
print(random_data)
```

---

### Combine DataFrames

#### `combine_dataframes(column_name, *dataframes)`
Combines multiple DataFrames based on a specified column into a new DataFrame, aligning by the index.

**Parameters:**
- `column_name`: `str`. The column to extract from each DataFrame.
- `*dataframes`: Multiple pandas DataFrames passed as positional arguments.

**Returns:**
- `pandas.DataFrame`. A new DataFrame combining the specified columns from all input DataFrames.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics as ec

df1 = pd.read_csv('data1.csv')
df2 = pd.read_csv('data2.csv')

combined_df = ec.combine_dataframes('Close', df1, df2)
print(combined_df)
```

---

### Financial Data Retrieval

#### `data(ticker_symbol, start_date, end_date, interval)`
Downloads financial data from Yahoo Finance and calculates daily returns.

**Parameters:**
- `ticker_symbol`: `str`. The stock ticker symbol.
- `start_date`: `str`. Start date in 'dd-mm-yyyy' format.
- `end_date`: `str`. End date in 'dd-mm-yyyy' format.
- `interval`: `str`. Data interval (e.g., '1d', '1wk', '1mo').

**Returns:**
- `pandas.DataFrame` containing the stock data and calculated returns.

**Example Usage:**
```python
from econkit import finance as f

start = '01-06-2024'
end = '07-06-2024'
interval = '1d'

df = f.data('AAPL', start, end, interval)
print(df.head())
```

---

## Usage Notes
- Ensure your data is clean and properly formatted before using these functions.
- Some functions handle missing values; specify your preferred method using the `handle_na` parameter.
- For time series analysis, ensure your data is indexed by date.

For further details, refer to the function docstrings in the source code or the examples provided above.
