import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

#  1. Understanding the Dataset 
data = loadmat('ex7data2.mat')
X = data['X']

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], s=30, alpha=0.7)
plt.title('Dataset Visualization')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

#  2. Finding Closest Centroids 
def find_closest_centroids(X, centroids):
    K = centroids.shape[0]
    idx = np.zeros(X.shape[0], dtype=int)
    
    for i in range(X.shape[0]):
        distances = np.sqrt(np.sum((X[i] - centroids) ** 2, axis=1))
        idx[i] = np.argmin(distances)
    
    return idx

initial_centroids = np.array([[3, 3], [6, 2], [8, 5]])
idx = find_closest_centroids(X, initial_centroids)
print("Closest centroids for first 3 points:", idx[:3])

#  3. Computing Centroids 
def compute_centroids(X, idx, K):
    centroids = np.zeros((K, X.shape[1]))
    
    for k in range(K):
        points = X[idx == k]
        if len(points) > 0:
            centroids[k] = np.mean(points, axis=0)
    
    return centroids

new_centroids = compute_centroids(X, idx, 3)
print("New centroids:\n", new_centroids)

#  4. Running K-means 
def run_k_means(X, initial_centroids, max_iters=10):
    K = initial_centroids.shape[0]
    centroids = initial_centroids.copy()
    
    for i in range(max_iters):
        idx = find_closest_centroids(X, centroids)
        centroids = compute_centroids(X, idx, K)
    
    return idx, centroids

idx, final_centroids = run_k_means(X, initial_centroids, max_iters=10)

# Visualization
colors = ['red', 'blue', 'green']
plt.figure(figsize=(8, 6))
for k in range(3):
    cluster_points = X[idx == k]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], 
                c=colors[k], s=30, alpha=0.6, label=f'Cluster {k}')
plt.scatter(final_centroids[:, 0], final_centroids[:, 1], 
            c='black', marker='x', s=200, linewidths=3, label='Centroids')
plt.title('K-means Clustering Results')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()

#  5. Initializing Centroids 
def init_centroids(X, K):
    m = X.shape[0]
    random_indices = np.random.choice(m, K, replace=False)
    centroids = X[random_indices]
    return centroids

K = 3
random_centroids = init_centroids(X, K)
print("Randomly initialized centroids:\n", random_centroids)

#  6. Testing with Different Initializations 
print("\n--- Testing with different initializations ---\n")
for run in range(3):
    print(f"Run {run + 1}:")
    init_cents = init_centroids(X, K)
    print("Initial centroids:\n", init_cents)
    final_idx, final_cents = run_k_means(X, init_cents, max_iters=10)
    print("Final centroids:\n", final_cents)
    
    # Calculate within-cluster sum of squares (inertia)
    inertia = 0
    for k in range(K):
        cluster_points = X[final_idx == k]
        if len(cluster_points) > 0:
            inertia += np.sum((cluster_points - final_cents[k]) ** 2)
    print(f"Inertia (WCSS): {inertia:.2f}\n")

#  7. Report: Cluster Assignments 
print("\n--- Cluster Assignment Report ---")
print(f"Dataset size: {X.shape[0]} points\n")
for i in range(min(20, X.shape[0])):
    print(f"Point {i}: {X[i]} -> Cluster {final_idx[i]}")
if X.shape[0] > 20:
    print(f"... and {X.shape[0] - 20} more points")