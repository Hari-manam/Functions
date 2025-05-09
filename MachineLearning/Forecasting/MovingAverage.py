import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(r"C:\Users\nanim\Downloads\airline-passengers.csv", parse_dates=['Month'], index_col='Month')

# === Moving Averages ===
df['Local_MA'] = df['Passengers'].rolling(window=3).mean()             # Short-term (Local)
df['Global_MA'] = df['Passengers'].rolling(window=13).mean()           # Long-term (Global)
df['Central_MA'] = df['Passengers'].rolling(window=5, center=True).mean()  # Symmetric smoothing
df['Trailing_MA'] = df['Passengers'].rolling(window=13).mean()         # Trailing window (same as global here)

# === Subplots ===
fig, axs = plt.subplots(5, 1, figsize=(14, 12), sharex=True)

# 1. Original
axs[0].plot(df['Passengers'], label='Original', color='black', linewidth=2)
axs[0].set_title('Original Series')
axs[0].legend()
axs[0].grid(True)

# 2. Local MA
axs[1].plot(df['Passengers'], label='Original', alpha=0.4, color='gray')
axs[1].plot(df['Local_MA'], label='Local MA (3)', color='orange')
axs[1].set_title('Local Moving Average (3 Months)')
axs[1].legend()
axs[1].grid(True)

# 3. Global MA
axs[2].plot(df['Passengers'], label='Original', alpha=0.4, color='gray')
axs[2].plot(df['Global_MA'], label='Global MA (13 Months)', color='blue')
axs[2].set_title('Global Moving Average (13 Months)')
axs[2].legend()
axs[2].grid(True)

# 4. Central MA
axs[3].plot(df['Passengers'], label='Original', alpha=0.4, color='gray')
axs[3].plot(df['Central_MA'], label='Central MA (Centered, 5)', color='green')
axs[3].set_title('Central Moving Average (5, Centered)')
axs[3].legend()
axs[3].grid(True)

# 5. Trailing MA
axs[4].plot(df['Passengers'], label='Original', alpha=0.4, color='gray')
axs[4].plot(df['Trailing_MA'], label='Trailing MA (13)', color='purple')
axs[4].set_title('Trailing Moving Average (13 Months)')
axs[4].legend()
axs[4].grid(True)

# === Formatting ===
for ax in axs:
    ax.tick_params(axis='x', rotation=45)

plt.suptitle("Moving Average Comparison: Local, Global, Central, Trailing", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
