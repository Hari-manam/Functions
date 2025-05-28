import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv(r'N:\ToyotaCorolla.csv')

# Identify categorical variables
categorical_cols = ['Model', 'Fuel_Type', 'Color']

# Convert categorical variables into dummy variables
df_dummies = pd.get_dummies(df[categorical_cols], drop_first=True)

# Combine dummy variables with numeric data
df_processed = pd.concat([df.drop(columns=categorical_cols + ['Id']), df_dummies], axis=1)

# Create correlation matrix
numeric_df = df_processed.select_dtypes(include=[np.number])
correlation_matrix = numeric_df.corr()

# Visualize correlation heatmap
plt.figure(figsize=(18, 14))
sns.heatmap(correlation_matrix, cmap='coolwarm', annot=False, fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix of Numeric Variables", fontsize=16)
plt.tight_layout()
plt.show()

# Show one record's dummy variables
print("Dummy Variables for First Record:")
df_dummies.iloc[0]
