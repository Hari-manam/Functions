import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

# === STEP 1: Load your dataset ===
df = pd.read_csv(r'N:\Natural_Gas_Consumptions.csv')  # Change path here

# === STEP 2: Filter for 'Adalar' and prepare time series ===
df_adalar = df[df['Districts'] == 'Adalar'].copy()
df_adalar['Date'] = pd.to_datetime(df_adalar[['Years', 'Months']].assign(DAY=1))
df_adalar.set_index('Date', inplace=True)
ts_adalar = df_adalar['Amounts_(m3)'].asfreq('MS')

# === STEP 3: Forecast using ARMA ===
ts_diff = ts_adalar.diff().dropna()
arma_model = ARIMA(ts_diff, order=(2, 0, 2)).fit()
arma_forecast = arma_model.forecast(steps=12)
arma_forecast_full = arma_forecast.cumsum() + ts_adalar.iloc[-1]
arma_dates = pd.date_range(start=ts_adalar.index[-1] + pd.offsets.MonthBegin(1), periods=12, freq='MS')

# Print ARMA Forecast
print("\n📘 ARMA Forecast:")
for date, value in zip(arma_dates, arma_forecast_full):
    print(f"{date.strftime('%Y-%m')}: {value:.2f} m³")

# === STEP 4: Forecast using ARIMA ===
arima_model = ARIMA(ts_adalar, order=(2, 1, 2)).fit()
arima_forecast = arima_model.forecast(steps=12)
arima_dates = arma_dates

# Print ARIMA Forecast
print("\n📗 ARIMA Forecast:")
for date, value in zip(arima_dates, arima_forecast):
    print(f"{date.strftime('%Y-%m')}: {value:.2f} m³")

# === STEP 5: Forecast using SARIMA ===
sarima_model = SARIMAX(ts_adalar, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)).fit()
sarima_forecast = sarima_model.forecast(steps=12)
sarima_dates = arma_dates

# Print SARIMA Forecast
print("\n📙 SARIMA Forecast:")
for date, value in zip(sarima_dates, sarima_forecast):
    print(f"{date.strftime('%Y-%m')}: {value:.2f} m³")

# === STEP 6: Plot all forecasts in separate subplots ===
fig, axs = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

# ARMA Plot
axs[0].plot(ts_adalar, label='Original', color='black')
axs[0].plot(arma_dates, arma_forecast_full, label='ARMA Forecast', color='orange', linestyle='--')
axs[0].set_title('ARMA (2,0,2) Forecast')
axs[0].legend()
axs[0].grid(True)

# ARIMA Plot
axs[1].plot(ts_adalar, label='Original', color='black')
axs[1].plot(arima_dates, arima_forecast, label='ARIMA (2,1,2) Forecast', color='green', linestyle='--')
axs[1].set_title('ARIMA (2,1,2) Forecast')
axs[1].legend()
axs[1].grid(True)

# SARIMA Plot
axs[2].plot(ts_adalar, label='Original', color='black')
axs[2].plot(sarima_dates, sarima_forecast, label='SARIMA (1,1,1)(1,1,1,12) Forecast', color='blue', linestyle='--')
axs[2].set_title('SARIMA Forecast')
axs[2].legend()
axs[2].grid(True)

plt.suptitle("Forecast Comparison: ARMA vs ARIMA vs SARIMA (Adalar)", fontsize=16)
plt.xticks(rotation=45)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
