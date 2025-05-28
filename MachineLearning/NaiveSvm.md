Naive Bayes Algorithm Notes
A probabilistic classification algorithm based on Bayes’ Theorem.
“Naive” because it assumes all features (e.g., words, measurements) are independent of each other given the class label, even though this isn’t always true.
Used for tasks like spam detection, sentiment analysis, and species classification.

Bayes’ Theorem
Formula:
P(A|B) = [P(B|A) * P(A)] / P(B)
P(A|B): Posterior probability (probability of class A given features B).
P(B|A): Likelihood (probability of features B given class A).
P(A): Prior probability (probability of class A before seeing features).
P(B): Evidence (probability of features B, often ignored in practice since it’s constant).
Naive Bayes uses this to calculate the probability of each class and picks the highest one.

Types of Naive Bayes
There are three main variants, each suited to different data types:

Gaussian Naive Bayes
Data Type: Continuous (e.g., height, weight).
Assumption: Features follow a Gaussian (normal) distribution.
Formula: P(x|class) = (1 / √(2πσ²)) * exp(-(x-μ)² / 2σ²)
(μ = mean, σ² = variance of feature for the class).
Example: Classifying Iris flowers based on petal length/width.
Multinomial Naive Bayes
Data Type: Discrete counts (e.g., word frequencies in text).
Assumption: Features represent counts or occurrences.
Use Case: Text classification (e.g., spam emails, movie reviews).
Example: Predicting if a review like “great movie” is positive.
Bernoulli Naive Bayes
Data Type: Binary/boolean (e.g., 1 = word present, 0 = absent).
Assumption: Features are binary variables.
Use Case: Binary text tasks (e.g., spam vs. not spam).
Example: Classifying “win free money” as spam based on word presence.

 How It Works
Training:
Calculate prior probabilities (P(class)) from the frequency of each class in the data.
Calculate likelihoods (P(feature|class)) for each feature given each class:
Gaussian: Use mean and variance.
Multinomial: Use feature counts.
Bernoulli: Use presence/absence probabilities.
Prediction:
For a new data point with features x₁, x₂, ..., xₙ:
Compute P(class|X) = P(class) * P(x₁|class) * P(x₂|class) * ... * P(xₙ|class) for each class.
Pick the class with the highest probability.
Often use log probabilities to avoid tiny numbers:
log(P(class|X)) = log(P(class)) + log(P(x₁|class)) + ...

 Key Features
Smoothing: Adds a small value (e.g., 1, called Laplace smoothing) to avoid zero probabilities for unseen features.
Example: P(word|class) = (count + 1) / (total + vocab_size).
Fast: Simple math, scales well with data.
Interpretable: You can see how probabilities contribute to decisions.

  Strengths
Simple and Fast: Quick to train and predict, even with big datasets.
Good with Small Data: Works well when you don’t have much training data.
Handles Text Well: Great for spam filters, sentiment analysis.
Robust: Performs decently even if the independence assumption is wrong.

 Weaknesses
Independence Assumption: Assumes features don’t affect each other, which is often false (e.g., “great” and “movie” in a review are related).
Zero Probability Problem: Without smoothing, unseen features ruin predictions.
Imbalanced Data: Can favor majority classes unless adjusted.
Limited Complexity: Struggles with intricate feature relationships (unlike SVM or neural networks).

 Practical Applications
Gaussian NB: Iris flower classification (continuous data).
Multinomial NB: Spam email detection, sentiment analysis (word counts).
Bernoulli NB: Document classification (word presence/absence).

 Example Datasets
Iris (Gaussian): Predict species (Setosa, Versicolor, Virginica) using petal/sepal measurements.
Text Reviews (Multinomial): Classify “I love this movie” as positive or negative based on word counts.
Emails (Bernoulli): Label “win free money” as spam or not based on word presence.

# Support Vector Machine (SVM) - Study Notes

## 1. Introduction to SVM
Support Vector Machine (SVM) is a **supervised learning algorithm** used for classification and regression tasks. It finds the **optimal hyperplane** that best separates different classes in a dataset.

## 2. Key Concepts
### 2.1 Hyperplane
- A **decision boundary** that separates different classes.
- In **2D space**, it's a line; in **3D space**, it's a plane.
- The best hyperplane is the one with the **maximum margin** between different classes.

### 2.2 Support Vectors
- The **data points closest to the hyperplane**.
- These points determine the position of the hyperplane.

### 2.3 Margin
- The distance between the hyperplane and the nearest data points from each class.
- **Maximizing margin** ensures better generalization of the model.

## 3. Types of SVM
### 3.1 Linear SVM
- Used when data is **linearly separable**.
- Finds a straight-line (or plane) decision boundary.

### 3.2 Non-Linear SVM
- Used when data is **not linearly separable**.
- Uses **kernels** to transform data into a higher-dimensional space.

## 4. SVM Kernels
### 4.1 Linear Kernel
- Used for **linearly separable** data.
- Equation: \( K(x_i, x_j) = x_i^T x_j \)

### 4.2 Polynomial Kernel
- Maps input data into a higher-degree polynomial feature space.
- Equation: \( K(x_i, x_j) = (x_i^T x_j + c)^d \)
- **Hyperparameters:**
  - **Degree (d)**: Controls polynomial complexity.
  - **Constant (c)**: Adjusts influence of higher-degree terms.

### 4.3 Radial Basis Function (RBF) Kernel
- Used for **highly non-linear** data.
- Maps data into an infinite-dimensional feature space.
- Equation: \( K(x_i, x_j) = \exp(-\gamma || x_i - x_j ||^2) \)
- **Hyperparameters:**
  - **Gamma (\(\gamma\))**: Controls influence of individual training examples.

### 4.4 Sigmoid Kernel
- Similar to activation function in neural networks.
- Equation: \( K(x_i, x_j) = \tanh(\alpha x_i^T x_j + c) \)

## 5. Hyperparameters in SVM
| Hyperparameter | Description |
|---------------|-------------|
| **C** | Regularization parameter (higher C = less margin, lower C = more generalization). |
| **Gamma (\(\gamma\))** | Determines influence of training points (higher \(\gamma\) = more localized decision boundary). |
| **Kernel** | Defines transformation function (Linear, Polynomial, RBF, Sigmoid). |
| **Degree (d)** | Used in Polynomial kernel to control feature transformation. |

## 6. Steps to Implement SVM
1. **Load the dataset** (e.g., Iris dataset).
2. **Preprocess the data** (feature scaling, missing value handling, encoding labels if needed).
3. **Split into training and test sets**.
4. **Choose a kernel** (linear, RBF, polynomial, or sigmoid).
5. **Train the SVM model** using `SVC()` from `sklearn`.
6. **Make predictions** on test data.
7. **Evaluate the model** using accuracy, confusion matrix, and classification report.
8. **Visualize decision boundaries** (if working with 2D data).

## 7. Example Code: SVM with Different Kernels
```python
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load dataset
iris = datasets.load_iris()
X = iris.data[:, :2]  # Using first two features for visualization
y = iris.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Experiment with different kernels
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
for kernel in kernels:
    model = SVC(kernel=kernel, C=1.0, gamma='scale')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Kernel: {kernel}, Accuracy: {accuracy:.4f}")
```

## 8. Visualization of Decision Boundaries
- **2D plots** can be used to visualize how each kernel separates the data.
- `matplotlib` and `numpy` help in creating **decision boundary plots**.

## 9. Advantages of SVM
✅ Effective for **high-dimensional spaces**.
✅ Works well when the number of **features is greater than the number of samples**.
✅ **Robust to overfitting** (if C parameter is tuned properly).

## 10. Disadvantages of SVM
❌ Computationally **expensive for large datasets**.
❌ **Not ideal for overlapping classes** (needs careful tuning of C & gamma).
❌ Difficult to interpret results compared to decision trees.

## 11. When to Use SVM?
🔹 When you have **small to medium-sized datasets**.  
🔹 When data is **high-dimensional**.  
🔹 When you need a **strong classifier for complex decision boundaries**.

## 12. Summary
- SVM is a powerful classification algorithm that works by **finding an optimal hyperplane**.
- Different **kernels** (Linear, RBF, Polynomial, Sigmoid) help handle **non-linear data**.
- Hyperparameters like **C, gamma, and kernel type** significantly impact performance.
- Works well for **small datasets**, but not ideal for **large-scale applications**.

---
**End of Notes - Happy Learning! 🚀**