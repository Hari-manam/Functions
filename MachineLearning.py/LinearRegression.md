Linear Regression Algorithm Notes
1. What is Linear Regression?
A supervised machine learning algorithm used to predict a continuous target variable based on one or more continuous or discrete features.
Models the relationship between features (independent variables) and the target (dependent variable) as a straight line (or plane in higher dimensions).
Used for tasks like predicting house prices, stock prices, or temperatures.

2. Types of Linear Regression
Simple Linear Regression:
One feature (e.g., x) to predict the target (y).
Equation: y = β₀ + β₁x + ε
β₀: Intercept (value of y when x = 0).
β₁: Slope (change in y per unit change in x).
ε: Error term.
Example: Predict house price (y) using square footage (x).
Multiple Linear Regression:
Multiple features (e.g., x₁, x₂, ...) to predict the target.
Equation: y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε
Example: Predict house price using square footage (x₁) and bedrooms (x₂).

3. How It Works
Model Representation:
Assumes a linear relationship: the target y changes linearly with the features.
Example: House_Price = 0.01 * Square_Footage + 2 * Bedrooms + intercept.
Training:
Goal: Find the best values for β₀, β₁, ... (coefficients) that minimize the error between predicted and actual values.
Method: Uses the least squares method to minimize the sum of squared residuals:
Error = Σ(y_actual - y_predicted)²
Solves for coefficients using mathematical optimization (e.g., normal equation or gradient descent).
Prediction:
For a new data point with features x₁, x₂, ..., compute:
y_pred = β₀ + β₁x₁ + β₂x₂ + ...
Example: For a house with 2000 sq ft and 3.5 bedrooms, predict the price using the fitted equation.

4. Key Assumptions
Linearity: The relationship between features and target is linear.
Independence: Observations are independent of each other.
Homoscedasticity: Constant variance of errors across all levels of features.
Normality: Errors are normally distributed (important for statistical tests).
No Multicollinearity: Features should not be highly correlated (in multiple regression).

5. Evaluation Metrics
R² Score: Measures how much variance in the target is explained by the model (0 to 1; 1 is perfect).
Example: R² = 0.85 means 85% of house price variation is explained.
Mean Squared Error (MSE): Average of squared differences between actual and predicted values.
Root Mean Squared Error (RMSE): Square root of MSE, in the same units as the target.

6. Strengths
Simple and Interpretable: Easy to understand; coefficients show feature impact (e.g., “+1 bedroom adds $20,000 to price”).
Fast: Quick to train and predict, even with large datasets.
Works Well with Linear Data: Effective when the relationship is truly linear.
Feature Importance: Coefficients indicate which features matter most.

7. Weaknesses
Assumes Linearity: Fails if the relationship is non-linear (e.g., exponential growth).
Sensitive to Outliers: Outliers can heavily skew the line.
Over-Simplifies: Can’t capture complex patterns (unlike neural networks).
Multicollinearity: If features are correlated, coefficients become unreliable.

8. Practical Applications
House Price Prediction: Predict prices based on square footage, bedrooms, etc.
Sales Forecasting: Estimate future sales using advertising spend and seasonality.
Financial Analysis: Predict stock prices or loan interest rates over time.
Science: Model relationships like temperature vs. ice cream sales.

9.Dataset
House Prices:
Features: Square_Footage (500-3000), Bedrooms (1.0-5.0).
Target: House_Price (in $10,000s).
Result: R² = 0.85, showing a good fit for linear data.

Comparison with Naive Bayes
Linear Regression:
Predicts continuous values (e.g., house prices).
Models a linear relationship using coefficients.
Discriminative: Directly models the relationship between features and target.
Naive Bayes:
Predicts categorical values (e.g., spam or not).
Probabilistic, assumes feature independence.
Generative: Models the data distribution for each class.