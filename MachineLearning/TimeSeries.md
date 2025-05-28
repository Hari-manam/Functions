Time Series Analysis (TSA) 
What is Time Series Analysis?
•	TSA involves analyzing data that is recorded over time.
•	Time order is crucial — past values affect future ones.
Importance of TSA
•	Forecast future values (e.g., stock prices, weather)
•	Detect trends, seasonality, anomalies
•	Useful in finance, retail, healthcare, energy, etc.
 Components of Time Series
Component	Description	Example
Trend	Long-term movement in data	Increasing temperature over years
Seasonality	Short-term repeated patterns (time-bound)	Higher electricity uses in summer
Cyclic	Irregular long-term fluctuations	Economic recessions and recoveries
White Noise	Random variations with no pattern	Sudden unexpected value (error/noise)
these essential transformation techniques used in time series analysis and machine learning, especially for improving model performance and stability.

1. Log Transformation
 What it is:
A non-linear transformation that compresses high values more than low values, reducing right skewness (when most data is small but there are a few large outliers).
(We add +1 to avoid log(0), which is undefined.)
Use it when:
•	Data has exponential growth (e.g., sales, population).
•	You want to reduce skewness.
•	Variance increases with the level of the series.
Caution:
•	Only works for positive values. Use log1p() in Python for safety.

2. Differencing
What it is:
A method to remove trends and seasonality by subtracting the previous value from the current one.
Use it when:
•	The series is non-stationary (mean or variance changes over time).
•	You need to stabilize the mean for models like ARIMA.
Can be applied multiple times:
•	1st order: remove trend
•	2nd order: remove acceleration (nonlinear trend)


3. Box-Cox Transformation
What it is:
A power transformation that can stabilize variance and make the data more normal-distributed.
•	The algorithm searches for the best λ (lambda) to transform your data.
Use it when:
•	Data is non-normal, heteroscedastic, or skewed.
•	You’re working with positive values only.


4. Yeo-Johnson Transformation
What it is:
An extension of Box-Cox that works with zero and negative values too.
A more flexible formula that internally switches between different transformations depending on the data sign and lambda.
Use it when:
•	You have zero or negative values in your data.
•	You still want to benefit from Box-Cox-like variance stabilization.

Key Concepts in TSA
1. Stationarity
•	A time series is stationary if:
o	Mean and variance are constant over time
o	No trends or seasonality
•	Why it matters: Many models assume stationarity
2. Autocorrelation
•	Measures how current values relate to past values
•	Helps detect seasonality and lag relationships
3. ACF & PACF
•	ACF (Autocorrelation Function): Correlation with all past values
•	PACF (Partial ACF): Correlation with specific lagged values (removes indirect effects)
•	Used to choose the right AR/MA terms
 Models in TSA
Model	Full Form	Purpose
AR	Auto-Regressive	Predicts using past values
MA	Moving Average	Predicts using past error terms
ARMA	AR + MA	For stationary data
ARIMA	AR + I (Differencing) + MA	For non-stationary data
SARIMA	ARIMA + Seasonal component	Handles both seasonality and trend

Common Techniques
•	Differencing: Removes trends, makes data stationary
•	Log Transformation: Reduces skewness
•	Box-Cox / Yeo-Johnson: Stabilizes variance
•	Decomposition: Breaks down time series into trend, seasonal, residual

Forecasting
•	Predict future values based on patterns in past data
•	Can be:
o	Point forecasts (e.g., next month’s sales = 500 units)
o	Interval forecasts (e.g., 95% chance sales will be 480–520)
 Identifying Patterns
•	Use plots:
o	Line plots for trends
o	Seasonal plots for cycles
o	ACF/PACF plots for lags
•	Use statistical tests:
o	Augmented Dickey-Fuller (ADF) test for stationarity

