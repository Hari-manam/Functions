📌 Banking Analytics Notes
1. Logistic Regression – Loan Default Prediction
Concept:
Logistic Regression is a classification algorithm used when the target variable is binary (e.g., default vs. no default).
It predicts the probability of an event occurring.
The logistic function (sigmoid) is used to transform linear outputs into probabilities.
Problem Statement:
A bank wants to predict whether a customer will default on a loan based on:

Credit Score
Annual Income
Loan Amount
This helps the bank decide whether to approve or reject loans.

2. Problem of Collinearity – Credit Risk Analysis
Concept:
Collinearity (Multicollinearity) occurs when independent variables are highly correlated.
It distorts regression coefficients and reduces model interpretability.
Problem Statement:
A bank wants to analyze credit risk using features such as:

Annual Income
Savings Balance
Credit Score
If Annual Income and Savings Balance are highly correlated, it might be difficult to determine which variable truly affects credit risk.
​
 
If VIF > 10, multicollinearity is a serious issue.
Solution:
Remove one of the correlated variables.
Use Principal Component Analysis (PCA) or regularization (Lasso regression).
3. WOE & IV – Fraud Detection
Concept:
Weight of Evidence (WOE): Measures the predictive power of a categorical variable.
Information Value (IV): Helps determine the importance of a variable.
Problem Statement:
A bank wants to detect fraudulent transactions based on:

Transaction Type (Online, ATM, POS, Wire Transfer)

Use Case:
A high IV value suggests the feature (e.g., transaction type) is highly predictive of fraud.
This helps banks flag risky transactions.
4. Residual Analysis – Bank Revenue Prediction
Concept:
Residuals are the difference between actual and predicted values.
A good model should have normally distributed residuals with constant variance.
Problem Statement:
A bank wants to predict revenue based on loan disbursement.

If residuals show patterns, it means the model is biased and missing key factors.
How to Check:
Residual Plot: Scatter plot of residuals vs. predicted values.
If randomly scattered, the model is good.
If pattern exists, the model needs improvement.
Solution:
Try adding more features.
Use non-linear transformations.
5. Heteroscedasticity – Interest Rate Prediction
Concept:
Heteroscedasticity means residual variance changes with the predictor.
Violates the assumption of constant variance in regression models.
Problem Statement:
A bank wants to predict interest rates based on customer income.

If higher incomes show lower variance in errors, it means the data is heteroscedastic.
How to Detect:
Breusch-Pagan Test: If p-value < 0.05, heteroscedasticity exists.
Residual Plot: If the spread of residuals increases with income, heteroscedasticity is present.
Solution:
Use log transformation or weighted least squares regression.
✅ Summary Table
Concept	Problem Statement	Key Check	Solution
Logistic Regression	Predict loan default	Accuracy, Classification Report	Improve features, regularization
Collinearity	Credit risk analysis	VIF > 10	Drop variables, PCA, Lasso
WOE & IV	Fraud detection	IV Score	Use high-IV features
Residual Analysis	Bank revenue prediction	Residual plot	Add missing features
Heteroscedasticity	Interest rate prediction	Breusch-Pagan Test	Log transformation
📝 Final Thoughts
Banks rely on these techniques to assess risk, detect fraud, and make better predictions.
Using WOE & IV helps in fraud analysis, while logistic regression is great for credit risk modeling.
Detecting collinearity and residual issues ensures robust models.
Heteroscedasticity detection prevents bias in predicting interest rates and financial outcomes.