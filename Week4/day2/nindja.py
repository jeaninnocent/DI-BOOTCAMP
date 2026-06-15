import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

#  PART 1: Image Compression with K-Means 

# 1.1 Load and preprocess image data
image_data = loadmat('bird_small.mat')
A = image_data['A']  # Shape: (128, 128, 3)

print(f"Original image shape: {A.shape}")
print(f"Original image size: {A.size} pixels")

# Normalize pixel values to range [0, 1]
A_normalized = A / 255.0

# Reshape into 2D array: each row = pixel, columns = RGB
original_shape = A_normalized.shape
X_img = A_normalized.reshape(-1, 3)
print(f"Reshaped data shape: {X_img.shape}")

# 1.2 K-Means functions (reused from previous exercise)
def find_closest_centroids(X, centroids):
    K = centroids.shape[0]
    idx = np.zeros(X.shape[0], dtype=int)
    
    for i in range(X.shape[0]):
        distances = np.sqrt(np.sum((X[i] - centroids) ** 2, axis=1))
        idx[i] = np.argmin(distances)
    
    return idx

def compute_centroids(X, idx, K):
    centroids = np.zeros((K, X.shape[1]))
    
    for k in range(K):
        points = X[idx == k]
        if len(points) > 0:
            centroids[k] = np.mean(points, axis=0)
    
    return centroids

def init_centroids(X, K):
    m = X.shape[0]
    random_indices = np.random.choice(m, K, replace=False)
    centroids = X[random_indices]
    return centroids

def run_k_means(X, initial_centroids, max_iters=10):
    K = initial_centroids.shape[0]
    centroids = initial_centroids.copy()
    
    for i in range(max_iters):
        idx = find_closest_centroids(X, centroids)
        centroids = compute_centroids(X, idx, K)
    
    return idx, centroids

# 1.3 Apply K-Means for image compression
K = 16  # Number of colors for compression
max_iters = 10

print(f"\nCompressing image to {K} colors...")

# Initialize centroids randomly
initial_centroids_img = init_centroids(X_img, K)

# Run K-Means
idx_img, centroids_img = run_k_means(X_img, initial_centroids_img, max_iters)

# 1.4 Recover compressed image
# Map each pixel to its closest centroid
X_recovered = centroids_img[idx_img]

# Reshape back to original image dimensions
img_compressed = X_recovered.reshape(original_shape)

# 1.5 Display original and compressed images
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(A_normalized)
plt.title(f'Original Image\n{original_shape[0]}x{original_shape[1]} pixels, 24-bit color')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(img_compressed)
plt.title(f'Compressed Image\n{K} colors, {K*3*8} bits total')
plt.axis('off')

plt.tight_layout()
plt.show()

print(f"\nCompression ratio: {24 / (np.log2(K) * 3):.2f}:1")
print(f"Original: 24 bits per pixel")
print(f"Compressed: {np.log2(K) * 3:.2f} bits per pixel")

#  PART 2: Dimensionality Reduction with PCA 

# 2.1 Load PCA dataset
pca_data = loadmat('ex7data1.mat')
X_pca = pca_data['X']

print(f"\nPCA dataset shape: {X_pca.shape}")

# 2.2 Visualize original data
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.scatter(X_pca[:, 0], X_pca[:, 1], s=30, alpha=0.7)
plt.title('Original PCA Dataset')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.axis('equal')

# 2.3 Implement PCA
def feature_normalize(X):
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)
    X_norm = (X - mu) / sigma
    return X_norm, mu, sigma

def pca(X):
    # Normalize features
    X_norm, mu, sigma = feature_normalize(X)
    
    # Compute covariance matrix
    m = X_norm.shape[0]
    Sigma = (1 / m) * (X_norm.T @ X_norm)
    
    # Perform SVD
    U, S, V = np.linalg.svd(Sigma)
    
    return U, S, X_norm, mu, sigma

# Apply PCA
U, S, X_norm, mu, sigma = pca(X_pca)

print(f"\nPrincipal components (U):\n{U}")
print(f"\nSingular values (S): {S}")

# 2.4 Project data onto first principal component
def project_data(X, U, K_dim):
    U_reduce = U[:, :K_dim]
    Z = X @ U_reduce
    return Z

def recover_data(Z, U, K_dim):
    U_reduce = U[:, :K_dim]
    X_recovered = Z @ U_reduce.T
    return X_recovered

# Project to 1 dimension
K_dim = 1
Z = project_data(X_norm, U, K_dim)
X_recovered_norm = recover_data(Z, U, K_dim)

# Denormalize recovered data
X_recovered = X_recovered_norm * sigma + mu

print(f"\nProjected data shape: {Z.shape}")
print(f"Recovered data shape: {X_recovered.shape}")

# 2.5 Visualize results
plt.subplot(1, 2, 2)
plt.scatter(X_pca[:, 0], X_pca[:, 1], s=30, alpha=0.5, label='Original')
plt.scatter(X_recovered[:, 0], X_recovered[:, 1], s=30, alpha=0.7, 
            color='red', marker='x', label='Recovered (1D)')

# Plot the principal component direction
mean_point = np.mean(X_pca, axis=0)
pc_direction = U[:, 0] * np.max(np.abs(X_pca - mean_point)) * 2
plt.plot([mean_point[0], mean_point[0] + pc_direction[0]], 
         [mean_point[1], mean_point[1] + pc_direction[1]], 
         'g-', linewidth=3, label='PC1 Direction')

plt.title('PCA: Original vs Recovered (1 component)')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.axis('equal')

plt.tight_layout()
plt.show()

# 2.6 Explained variance
explained_variance = (S / np.sum(S)) * 100
cumulative_variance = np.cumsum(explained_variance)

print("\n--- Explained Variance ---")
for i, var in enumerate(explained_variance):
    print(f"PC{i+1}: {var:.2f}%")
print(f"Cumulative variance with 1 component: {cumulative_variance[0]:.2f}%")
print(f"Cumulative variance with 2 components: {cumulative_variance[1]:.2f}%")

# Optional: Try with 2 dimensions (full reconstruction)
Z_2d = project_data(X_norm, U, 2)
X_recovered_full = recover_data(Z_2d, U, 2)
X_recovered_full = X_recovered_full * sigma + mu

# Verify perfect reconstruction with 2 components
reconstruction_error = np.mean((X_pca - X_recovered_full) ** 2)
print(f"\nReconstruction error with 2 components: {reconstruction_error:.2e}")

#  Bonus: Different compression levels for image 
print("\n--- Image Compression with different K values ---")
K_values = [2, 4, 8, 16, 32, 64]

plt.figure(figsize=(15, 10))
for idx, K in enumerate(K_values):
    initial_cents = init_centroids(X_img, K)
    idx_temp, cents_temp = run_k_means(X_img, initial_cents, max_iters=10)
    X_temp_recovered = cents_temp[idx_temp]
    img_temp = X_temp_recovered.reshape(original_shape)
    
    plt.subplot(2, 3, idx + 1)
    plt.imshow(img_temp)
    plt.title(f'{K} colors\n{np.log2(K)*3:.2f} bits/pixel')
    plt.axis('off')

plt.suptitle('Image Compression with Different Color Quantization Levels', fontsize=14)
plt.tight_layout()
plt.show()