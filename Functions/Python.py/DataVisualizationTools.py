# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Load dataset (Modify path if needed)
file_path = r"C:\Users\nanim\OneDrive\Desktop\Datasets\healthcare-dataset-stroke-data.csv"  # Ensure the file is in the same directory or update path
df = pd.read_csv(file_path)

# Keep only relevant columns
df = df[['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'stroke']]

# Fill missing BMI values with median
df['bmi'].fillna(df['bmi'].median(), inplace=True)

# Convert 'stroke' to categorical string for easy visualization
df['stroke'] = df['stroke'].astype(str)

# -------------------------------
# 📊 Simple & Easy-to-Understand Graphs
# -------------------------------

## 1️⃣ **Bar Plot: Count of Stroke vs. Non-Stroke Cases**
plt.figure(figsize=(6,5))
sns.countplot(x=df['stroke'], palette=['blue', 'red'])
plt.xlabel("Stroke (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.title("Count of Stroke vs. Non-Stroke Cases")
plt.xticks(ticks=[0,1], labels=["No Stroke", "Stroke"])
plt.show()

## 2️⃣ **Histogram: Age Distribution by Stroke Status**
plt.figure(figsize=(10,5))
sns.histplot(df[df['stroke'] == '0']['age'], kde=True, color='blue', label="No Stroke", bins=30)
sns.histplot(df[df['stroke'] == '1']['age'], kde=True, color='red', label="Stroke", bins=30)
plt.xlabel("Age")
plt.ylabel("Count")
plt.title("Age Distribution for Stroke vs. Non-Stroke Patients")
plt.legend()
plt.show()

## 3️⃣ **Box Plot: Glucose Levels in Stroke vs. Non-Stroke Patients**
plt.figure(figsize=(8,5))
sns.boxplot(x=df['stroke'], y=df['avg_glucose_level'], palette=['blue', 'red'])
plt.xlabel("Stroke (0 = No, 1 = Yes)")
plt.ylabel("Average Glucose Level")
plt.title("Glucose Levels for Stroke vs. Non-Stroke Patients")
plt.show()

## 4️⃣ **Scatter Plot: BMI vs. Glucose Levels (Color by Stroke)**
plt.figure(figsize=(8,5))
sns.scatterplot(data=df, x='bmi', y='avg_glucose_level', hue='stroke', alpha=0.7, palette=['blue', 'red'])
plt.xlabel("BMI")
plt.ylabel("Average Glucose Level")
plt.title("BMI vs. Glucose Levels (Stroke vs. Non-Stroke)")
plt.legend(title="Stroke", labels=["No Stroke", "Stroke"])
plt.show()

## 5️⃣ **Heatmap: Correlation Between Health Factors**
plt.figure(figsize=(8,6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Between Different Health Factors")
plt.show()

## 6️⃣ **Pie Chart: Stroke vs. Non-Stroke Percentage**
plt.figure(figsize=(6,6))
df['stroke'].value_counts().plot.pie(autopct='%1.1f%%', labels=["No Stroke", "Stroke"], colors=['blue', 'red'], startangle=90, wedgeprops={'edgecolor': 'black'})
plt.title("Stroke vs. Non-Stroke Distribution")
plt.ylabel("")
plt.show()

## 7️⃣ **KDE Plot: BMI Distribution in Stroke vs. Non-Stroke Patients**
plt.figure(figsize=(8,5))
sns.kdeplot(df[df['stroke'] == '0']['bmi'], label='No Stroke', color='blue', fill=True)
sns.kdeplot(df[df['stroke'] == '1']['bmi'], label='Stroke', color='red', fill=True)
plt.xlabel("BMI")
plt.ylabel("Density")
plt.title("BMI Distribution for Stroke vs. Non-Stroke Patients")
plt.legend()
plt.show()

## 8️⃣ **Violin Plot: BMI Distribution for Stroke vs. Non-Stroke**
plt.figure(figsize=(8,5))
sns.violinplot(x=df['stroke'], y=df['bmi'], palette=['blue', 'red'])
plt.xlabel("Stroke (0 = No, 1 = Yes)")
plt.ylabel("BMI")
plt.title("BMI Distribution for Stroke vs. Non-Stroke Patients")
plt.show()

## 9️⃣ **Line Plot: Age vs. Average Glucose Level (Grouped by Stroke Status)**
plt.figure(figsize=(10,5))
sns.lineplot(data=df, x="age", y="avg_glucose_level", hue="stroke", palette=['blue', 'red'])
plt.xlabel("Age")
plt.ylabel("Average Glucose Level")
plt.title("Age vs. Glucose Level (Stroke vs. Non-Stroke)")
plt.legend(title="Stroke", labels=["No Stroke", "Stroke"])
plt.show()

## 🔟 **Swarm Plot: Glucose Levels by Stroke Status**
plt.figure(figsize=(10,5))
sns.swarmplot(x="stroke", y="avg_glucose_level", data=df, palette=['blue', 'red'])
plt.xlabel("Stroke (0 = No, 1 = Yes)")
plt.ylabel("Average Glucose Level")
plt.title("Swarm Plot: Glucose Levels in Stroke vs. Non-Stroke")
plt.show()

# -------------------------------
# 📈 Using Normal Distribution to Find Probability of Stroke Based on Glucose Level
# -------------------------------

# Fit normal distribution for glucose levels
mu, sigma = norm.fit(df['avg_glucose_level'])

# Plot histogram with normal distribution
plt.figure(figsize=(10,5))
sns.histplot(df['avg_glucose_level'], bins=30, kde=False, color='blue', label="Glucose Data", stat="density")

# Generate normal distribution curve
x = np.linspace(df['avg_glucose_level'].min(), df['avg_glucose_level'].max(), 100)
plt.plot(x, norm.pdf(x, mu, sigma), color='red', label=f"Normal Fit (μ={mu:.2f}, σ={sigma:.2f})")

plt.xlabel("Average Glucose Level")
plt.ylabel("Density")
plt.title("Normal Distribution Fit for Glucose Levels")
plt.legend()
plt.show()

# Compute probability of stroke given high glucose levels (Z-score > 2)
z_score_threshold = 2
high_glucose_threshold = mu + z_score_threshold * sigma

# Count the number of people with glucose levels above the threshold
high_glucose_count = (df['avg_glucose_level'] > high_glucose_threshold).sum()
total_count = len(df)

# Probability calculation
stroke_probability = high_glucose_count / total_count

print(f"Probability of stroke for individuals with high glucose levels (Z-Score > 2): {stroke_probability:.4f}")
