# robot position transformation
import numpy as np

# Initial position of the robot (x, y)
initial_position = np.array([2, 3])

# Transformation matrix (e.g., translation by (dx, dy))
# For example, translating by (1, 2)
transformation_matrix = np.array([
    [1, 0, 1],  # Translation in x-direction by 1
    [0, 1, 2],  # Translation in y-direction by 2
    [0, 0, 1]   # Homogeneous coordinate
])

# Convert initial position to homogeneous coordinates (x, y, 1)
initial_position_homogeneous = np.append(initial_position, 1)

# Calculate the target position using matrix multiplication
target_position_homogeneous = np.dot(transformation_matrix, initial_position_homogeneous)

# Extract the target position (x, y) from homogeneous coordinates
target_position = target_position_homogeneous[:2]

print(f"Initial Position: {initial_position}")
print(f"Transformation Matrix:\n{transformation_matrix}")
print(f"Target Position: {target_position}")

# Netflix Recommendations

import numpy as np
from sklearn.decomposition import NMF

# User-Item Matrix (rows: users, columns: movies, values: ratings)
# 0 indicates missing ratings
user_item_matrix = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [1, 0, 0, 4],
    [0, 1, 5, 4],
])

# Number of latent features
n_features = 2

# Apply Non-negative Matrix Factorization (NMF)
model = NMF(n_components=n_features, init='random', random_state=42)
user_features = model.fit_transform(user_item_matrix)
item_features = model.components_

# Predict the missing ratings
predicted_ratings = np.dot(user_features, item_features)

# Recommend movies for a specific user (e.g., user 0)
user_index = 0
user_ratings = predicted_ratings[user_index]
recommended_movies = np.argsort(user_ratings)[::-1]  # Sort movies by predicted rating

print(f"User-Item Matrix:\n{user_item_matrix}")
print(f"Predicted Ratings:\n{predicted_ratings}")
print(f"Recommended Movies for User {user_index}: {recommended_movies}")

# Display the top recommended movie
top_movie_index = recommended_movies[0]
print(f"Top Recommended Movie for User {user_index}: Movie {top_movie_index}")

# matrices are used to secure the data

import numpy as np

# Original data (as a vector)
data = np.array([7, 4])

# Encryption matrix (must be invertible)
encryption_matrix = np.array([
    [2, 3],
    [1, 4]
])

# Encrypt the data
encrypted_data = np.dot(encryption_matrix, data)

# Decryption matrix (inverse of the encryption matrix)
decryption_matrix = np.linalg.inv(encryption_matrix)

# Decrypt the data
decrypted_data = np.dot(decryption_matrix, encrypted_data)

print(f"Original Data: {data}")
print(f"Encryption Matrix:\n{encryption_matrix}")
print(f"Encrypted Data: {encrypted_data}")
print(f"Decryption Matrix:\n{decryption_matrix}")
print(f"Decrypted Data: {decrypted_data}")

# vector representation of velocity

import numpy as np

# Velocity of the car (magnitude 60 km/h, direction north)
velocity_vector = np.array([0, 60])

print(f"Velocity Vector: {velocity_vector}")

