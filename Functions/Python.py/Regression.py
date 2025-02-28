import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Sample Data
data = {
    'Credit_Score': [750, 680, 720, 580, 640, 530, 810, 670, 590, 720],
    'Income': [50000, 60000, 70000, 35000, 45000, 30000, 90000, 62000, 40000, 72000],
    'Loan_Amount': [20000, 25000, 30000, 18000, 22000, 15000, 40000, 26000, 20000, 32000],
    'Default': [0, 0, 0, 1, 1, 1, 0, 0, 1, 0]  # 1 = Default, 0 = No Default
}

df = pd.DataFrame(data)

# Splitting data
X = df[['Credit_Score', 'Income', 'Loan_Amount']]
y = df['Default']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Logistic Regression Model
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Model Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
