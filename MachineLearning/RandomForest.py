# Random Forest Classifier with K-Fold Cross-Validation and Visualization on Stroke Dataset

# Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import LabelEncoder

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

# Define features and target
X = data.drop(['id', 'stroke'], axis=1)
y = data['stroke']

# Initialize the Random Forest classifier
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Set up K-Fold Cross-Validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Perform cross-validation
cv_scores = cross_val_score(rf_clf, X, y, cv=kf, scoring='accuracy')

# Output results
print("Cross-validation scores:", cv_scores)
print(f"Average accuracy: {cv_scores.mean():.2f}")

# Visualization
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
sns.barplot(x=list(range(1, 6)), y=cv_scores)
plt.title('Random Forest Classifier Cross-Validation Scores')
plt.xlabel('Fold')
plt.ylabel('Accuracy')
plt.ylim(0, 1)
plt.show()
