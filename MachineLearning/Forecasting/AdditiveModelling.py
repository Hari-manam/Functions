import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Step 1: Load the Airline Passengers dataset
df = pd.read_csv(r"C:\Users\nanim\Downloads\airline-passengers.csv", parse_dates=['Month'], index_col='Month')
df = df[['Passengers']].dropna()

# Step 2: Apply multiplicative decomposition (monthly seasonality)
result = seasonal_decompose(df['Passengers'], model='multiplicative', period=12)

# Step 3: Improved plot (similar to your AAPL example)
fig, axs = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
components = ['observed', 'trend', 'seasonal', 'resid']
titles = ['Observed', 'Trend', 'Seasonal', 'Residual']

for i, comp in enumerate(components):
    axs[i].plot(getattr(result, comp), color='tab:blue', marker='o' if comp == 'resid' else None)
    axs[i].set_title(f'{titles[i]} (Multiplicative)', fontsize=12)
    axs[i].grid(True)
    axs[i].tick_params(axis='x', rotation=45)

plt.suptitle("Multiplicative Decomposition of Monthly Airline Passengers", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

