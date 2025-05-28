# Decision Tree Visualization and Accuracy Calculation for Stroke Dataset

# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

# Load dataset
data = pd.read_csv(r'C:\Users\nanim\OneDrive\Desktop\Datasets\healthcare-dataset-stroke-data.csv')

# Data preprocessing
# Drop rows with missing values
data = data.dropna()

# Encoding categorical features
categorical_columns = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Selecting two features for visualization
X_features = ['age', 'avg_glucose_level']

# Defining features and target
X = data[X_features]
y = data['stroke']

# Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)

# Cross-validation to calculate accuracy scores
cv_scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
average_accuracy = np.mean(cv_scores)

print("Cross-validation scores:", cv_scores)
print(f"Average accuracy: {average_accuracy:.2f}")

# Visualization
labels = np.where(y == 1, 'Stroke', 'No Stroke')

plt.figure(figsize=(10, 7))
for i in range(len(X)):
    color = 'red' if labels[i] == 'Stroke' else 'green'
    plt.scatter(X.iloc[i, 0], X.iloc[i, 1], color=color, s=50, edgecolors='black', alpha=0.7,
                label=labels[i] if labels[i] not in plt.gca().get_legend_handles_labels()[1] else "")

boundary_age = 60
plt.axvline(x=boundary_age, color="blue", linestyle="--", linewidth=2, label=f"Age = {boundary_age} (Decision Boundary)")
plt.text(boundary_age + 1, max(X.iloc[:, 1])*0.7, f"Age > {boundary_age}?", color="blue", fontsize=12, rotation=90, verticalalignment='center')

plt.xlabel("Age")
plt.ylabel("Average Glucose Level")
plt.title("Decision Tree Split for Stroke Prediction")
plt.legend()
plt.grid(True)

plt.show()