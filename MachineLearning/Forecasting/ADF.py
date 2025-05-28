import pandas as pd
from statsmodels.tsa.stattools import adfuller

# === Load dataset ===
df = pd.read_csv(r'N:\Natural_Gas_Consumptions.csv')  # Update the path

# === Prepare Adalar time series ===
df_adalar = df[df['Districts'] == 'Adalar'].copy()
df_adalar['Date'] = pd.to_datetime(df_adalar[['Years', 'Months']].assign(DAY=1))
df_adalar.set_index('Date', inplace=True)
ts_adalar = df_adalar['Amounts_(m3)'].asfreq('MS')

# === Apply ADF test ===
result = adfuller(ts_adalar)

# === Print Results ===
print("ADF Test Result on Original Series:")
print(f"ADF Statistic: {result[0]}")
print(f"p-value: {result[1]}")
for key, value in result[4].items():
    print(f"Critical Value ({key}): {value}")

# === Conclusion ===
if result[1] < 0.05:
    print("✅ The series is stationary (no differencing needed).")
else:
    print("❌ The series is non-stationary (apply differencing).")
