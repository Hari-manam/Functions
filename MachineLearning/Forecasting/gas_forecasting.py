import pandas as pd
from prophet import Prophet
import pmdarima as pm
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import numpy as np

# Load your data
df = pd.read_csv(r"N:\Natural_Gas_Consumptions.csv")

# Filter for Adalar
adalar_df = df[df['Districts'] == 'Adalar'].copy()
adalar_df['ds'] = pd.to_datetime(adalar_df['Years'].astype(str) + '-' + adalar_df['Months'].astype(str) + '-01')
adalar_df = adalar_df.rename(columns={'Amounts_(m3)': 'y'})
adalar_df = adalar_df[['ds', 'y']].sort_values('ds').reset_index(drop=True)

# Prophet
prophet_model = Prophet()
prophet_model.fit(adalar_df)
future = prophet_model.make_future_dataframe(periods=12, freq='MS')
forecast_prophet = prophet_model.predict(future)
prophet_forecast = forecast_prophet[['ds', 'yhat']].tail(12).set_index('ds')

# ARIMA
arima_model = pm.auto_arima(adalar_df['y'], seasonal=False, stepwise=True, suppress_warnings=True)
arima_forecast = arima_model.predict(n_periods=12)

# SARIMA
sarima_model = pm.auto_arima(adalar_df['y'], seasonal=True, m=12, stepwise=True, suppress_warnings=True)
sarima_forecast = sarima_model.predict(n_periods=12)

# Forecast dates
forecast_dates = pd.date_range(start=adalar_df['ds'].max() + pd.offsets.MonthBegin(), periods=12, freq='MS')

# Combine forecasts
comparison_df = pd.DataFrame({
    'ds': forecast_dates,
    'Prophet': prophet_forecast['yhat'].values,
    'ARIMA': arima_forecast,
    'SARIMA': sarima_forecast
}).set_index('ds')

# Plot comparison
comparison_df.plot(figsize=(12, 6), marker='o')
plt.title('Forecast Comparison - Adalar (Next 12 Months)')
plt.xlabel('Date')
plt.ylabel('Natural Gas Consumption (m³)')
plt.grid(True)
plt.show()
