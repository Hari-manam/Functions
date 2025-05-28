import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load a 2D dataset (Iris with only 2 features for visualization)
iris = datasets.load_iris()
X = iris.data[:, :2]  # Taking only the first two features (sepal length & width)
y = iris.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define different kernels to test
kernels = ['linear', 'poly', 'rbf', 'sigmoid']

# Create a figure for subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Loop through each kernel
for i, kernel in enumerate(kernels):
    # Train SVM model
    model = SVC(kernel=kernel, C=1.0, gamma='scale', degree=3)  # Adjust degree for poly
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Kernel: {kernel}, Accuracy: {accuracy:.4f}")

    # Create a mesh grid for visualization
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                         np.linspace(y_min, y_max, 100))
    
    # Predict on grid points
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot decision boundary
    ax = axes[i // 2, i % 2]
    ax.contourf(xx, yy, Z, alpha=0.3)
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, edgecolors='k', marker='o', label="Train")
    ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, edgecolors='k', marker='s', label="Test")
    ax.set_title(f"SVM with {kernel} kernel\nAccuracy: {accuracy:.4f}")
    ax.set_xlabel('Sepal Length')
    ax.set_ylabel('Sepal Width')

plt.legend()
plt.tight_layout()
plt.show()
