# Story: A bank wants to analyze customer behavior for loan approvals and fraud detection.
# They collect data on customer transactions, credit scores, and loan repayments.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Step 1: Generate Synthetic Banking Data
data = {
    'Customer_ID': np.arange(1, 11),
    'Credit_Score': [750, 620, 580, 690, 710, 680, 720, 600, 640, 580],
    'Monthly_Transactions': [30, 45, 10, 25, 40, 28, 35, 15, 20, 12],
    'Loan_Approval': [1, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    'Fraudulent_Activity': [0, 1, 0, 0, 0, 0, 0, 1, 0, 1]
}

df = pd.DataFrame(data)
print("Customer Data:\n", df)

# Step 2: Association and Dependence - Checking credit score and loan approval
dependency = df[['Credit_Score', 'Loan_Approval']].corr()
print("\nAssociation & Dependence between Credit Score and Loan Approval:\n", dependency)

# Step 3: Causation vs. Correlation - Does a high credit score mean a loan approval?
print("\nCorrelation between Credit Score and Loan Approval does not mean causation.")
print("Other factors like debt-to-income ratio and income stability impact loan approval.")

# Step 4: Covariance - Credit Score vs Monthly Transactions
cov_matrix = np.cov(df['Credit_Score'], df['Monthly_Transactions'])
print("\nCovariance between Credit Score and Monthly Transactions:\n", cov_matrix)

# Step 5: Simpson's Paradox - Loan Approval based on a hidden variable (Fraudulent Activity)
grouped = df.groupby('Fraudulent_Activity')[['Credit_Score', 'Loan_Approval']].mean()
print("\nSimpson's Paradox Analysis:\n", grouped)
print("\nEven with a high credit score, if a customer has fraudulent activity, loan approvals are lower.")

# Step 6: Clustering - Segmenting Customers Based on Credit Score and Transactions
X = df[['Credit_Score', 'Monthly_Transactions']]
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
df['Cluster'] = kmeans.labels_
print("\nCustomer Segmentation Using Clustering:\n", df[['Customer_ID', 'Cluster']])

# Step 7: Visualization of Clusters
plt.scatter(df['Credit_Score'], df['Monthly_Transactions'], c=df['Cluster'], cmap='viridis')
plt.xlabel('Credit Score')
plt.ylabel('Monthly Transactions')
plt.title('Customer Segmentation Based on Credit Score & Transactions')
plt.colorbar(label='Cluster')
plt.show()
