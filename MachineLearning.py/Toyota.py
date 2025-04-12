import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# Step 1: Load the dataset
df = pd.read_csv(r'N:\ToyotaCorolla.csv')

# Step 2: Identify categorical variables
categorical_cols = ['Model', 'Fuel_Type', 'Color']

# Step 3: Convert categorical variables into dummy variables (drop first to avoid multicollinearity)
df_dummies = pd.get_dummies(df[categorical_cols], drop_first=True)

# Step 4: Combine dummy variables with the original data (excluding original categorical columns)
df_processed = pd.concat([df.drop(columns=categorical_cols), df_dummies], axis=1)

# Step 5: (Optional) Drop ID column (not useful for modeling or PCA)
df_processed.drop(columns=['Id'], inplace=True)

# Step 6: Create correlation matrix
numeric_df = df_processed.select_dtypes(include=[np.number])
correlation_matrix = numeric_df.corr()

# Step 7: Plot correlation matrix
plt.figure(figsize=(15, 12))
sns.heatmap(correlation_matrix, cmap='coolwarm', linewidths=0.5)
plt.title("Correlation Matrix of Numeric Variables", fontsize=16)
plt.tight_layout()
plt.show()

# Step 8: (Optional) Standardize the dataset for PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(numeric_df)

# (Optional) Print one row's dummy variables for explanation
print("Dummy Variables for Record 1:\n", df_dummies.iloc[0])
