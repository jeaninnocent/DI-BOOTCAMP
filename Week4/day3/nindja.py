#  EXERCISE 1: Create a simple Convolutional Neural Network (CNN) 

# 1. Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Sequential
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
import warnings
warnings.filterwarnings('ignore')

print(f"TensorFlow version: {tf.__version__}")
print(f"Keras version: {keras.__version__}")

# 2. Load the dataset
# Note: Using a standard dataset suitable for CNN - we'll use Fashion MNIST
# which is built into Keras and works well for CNN demonstrations
print("\n" + "="*60)
print("LOADING DATASET")
print("="*60)

# Load Fashion MNIST dataset (28x28 grayscale images of clothing)
(X_train_full, y_train_full), (X_test, y_test) = keras.datasets.fashion_mnist.load_data()

# Take a subset for faster training (optional - comment out if you want full dataset)
# X_train_full = X_train_full[:10000]
# y_train_full = y_train_full[:10000]

print(f"Training data shape: {X_train_full.shape}")
print(f"Training labels shape: {y_train_full.shape}")
print(f"Test data shape: {X_test.shape}")
print(f"Test labels shape: {y_test.shape}")

# Class labels for Fashion MNIST
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Visualize sample images
plt.figure(figsize=(12, 8))
for i in range(16):
    plt.subplot(4, 4, i+1)
    plt.imshow(X_train_full[i], cmap='gray')
    plt.title(class_names[y_train_full[i]])
    plt.axis('off')
plt.suptitle('Sample Images from Dataset', fontsize=14)
plt.tight_layout()
plt.show()

# 3. Encode labels and scale features
print("\n" + "="*60)
print("DATA PREPROCESSING")
print("="*60)

# Normalize pixel values to range [0, 1]
X_train_scaled = X_train_full.astype('float32') / 255.0
X_test_scaled = X_test.astype('float32') / 255.0

# Reshape data for CNN (add channel dimension)
# CNNs expect shape: (samples, height, width, channels)
X_train_cnn = X_train_scaled.reshape(X_train_scaled.shape[0], 28, 28, 1)
X_test_cnn = X_test_scaled.reshape(X_test_scaled.shape[0], 28, 28, 1)

print(f"Reshaped training data: {X_train_cnn.shape}")
print(f"Reshaped test data: {X_test_cnn.shape}")

# Encode labels (convert to categorical for multi-class classification)
y_train_encoded = to_categorical(y_train_full, 10)
y_test_encoded = to_categorical(y_test, 10)

print(f"Encoded labels shape: {y_train_encoded.shape}")

# Split training data into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    X_train_cnn, y_train_encoded, test_size=0.2, random_state=42, stratify=y_train_full
)

print(f"\nFinal splits:")
print(f"Training: {X_train.shape}")
print(f"Validation: {X_val.shape}")
print(f"Test: {X_test_cnn.shape}")

# 4. Create Neural Network Model using .sequential()
print("\n" + "="*60)
print("BUILDING CNN MODEL")
print("="*60)

model = Sequential([
    # First Convolutional Block
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.BatchNormalization(),
    
    # Second Convolutional Block
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.BatchNormalization(),
    
    # Third Convolutional Block
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.BatchNormalization(),
    
    # Flatten and Dense Layers
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(10, activation='softmax')  # 10 classes for Fashion MNIST
])

# Display model architecture
model.summary()

# Visualize model architecture
keras.utils.plot_model(model, show_shapes=True, show_layer_names=True)

# 5. Compile and Train model
print("\n" + "="*60)
print("COMPILING MODEL")
print("="*60)

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("Model compiled successfully!")
print(f"Optimizer: Adam (lr=0.001)")
print(f"Loss function: Categorical Crossentropy")
print(f"Metrics: Accuracy")

print("\n" + "="*60)
print("TRAINING MODEL")
print("="*60)

# Train the model
history = model.fit(
    X_train, y_train,
    batch_size=64,
    epochs=15,
    validation_data=(X_val, y_val),
    verbose=1
)

# 6. Evaluate model's loss and accuracy
print("\n" + "="*60)
print("MODEL EVALUATION")
print("="*60)

# Evaluate on test set
test_loss, test_accuracy = model.evaluate(X_test_cnn, y_test_encoded, verbose=0)

print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

# Make predictions
y_pred_proba = model.predict(X_test_cnn, verbose=0)
y_pred = np.argmax(y_pred_proba, axis=1)
y_true = np.argmax(y_test_encoded, axis=1)

# Calculate additional metrics
accuracy = accuracy_score(y_true, y_pred)
print(f"\nClassification Accuracy: {accuracy:.4f}")

print(f"\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=class_names))

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix', fontsize=14)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.tight_layout()
plt.show()

#  TRAINING HISTORY VISUALIZATION 
print("\n" + "="*60)
print("TRAINING HISTORY ANALYSIS")
print("="*60)

# Plot training history
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy plot
axes[0].plot(history.history['accuracy'], label='Training Accuracy', marker='o')
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', marker='o')
axes[0].set_title('Model Accuracy', fontsize=12)
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

# Loss plot
axes[1].plot(history.history['loss'], label='Training Loss', marker='o')
axes[1].plot(history.history['val_loss'], label='Validation Loss', marker='o')
axes[1].set_title('Model Loss', fontsize=12)
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)

plt.suptitle('Training History', fontsize=14)
plt.tight_layout()
plt.show()

# Print final metrics
print(f"\nFinal Training Accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")
print(f"Final Test Accuracy: {test_accuracy:.4f}")
print(f"\nFinal Training Loss: {history.history['loss'][-1]:.4f}")
print(f"Final Validation Loss: {history.history['val_loss'][-1]:.4f}")
print(f"Final Test Loss: {test_loss:.4f}")

#  VISUALIZE PREDICTIONS 
print("\n" + "="*60)
print("SAMPLE PREDICTIONS")
print("="*60)

# Display some test images with predictions
n_samples = 16
plt.figure(figsize=(15, 12))

for i in range(n_samples):
    plt.subplot(4, 4, i+1)
    plt.imshow(X_test[i], cmap='gray')
    true_label = class_names[y_true[i]]
    pred_label = class_names[y_pred[i]]
    color = 'green' if true_label == pred_label else 'red'
    plt.title(f'True: {true_label}\nPred: {pred_label}', color=color, fontsize=10)
    plt.axis('off')

plt.suptitle('Sample Predictions (Green=Correct, Red=Incorrect)', fontsize=14)
plt.tight_layout()
plt.show()

#  MODEL PERFORMANCE SUMMARY 
print("\n" + "="*60)
print("MODEL PERFORMANCE SUMMARY")
print("="*60)

summary_data = {
    'Metric': ['Test Accuracy', 'Test Loss', 'Training Epochs', 'Batch Size', 'Learning Rate'],
    'Value': [f'{test_accuracy:.4f}', f'{test_loss:.4f}', '15', '64', '0.001']
}

summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))

# Check for overfitting
accuracy_gap = history.history['accuracy'][-1] - history.history['val_accuracy'][-1]
loss_gap = history.history['val_loss'][-1] - history.history['loss'][-1]

print(f"\nOverfitting Analysis:")
print(f"Training vs Validation Accuracy gap: {accuracy_gap:.4f}")
print(f"Validation vs Training Loss gap: {loss_gap:.4f}")

if accuracy_gap > 0.1:
    print("⚠️ Possible overfitting detected (accuracy gap > 0.1)")
elif accuracy_gap < -0.05:
    print("⚠️ Possible underfitting detected (validation accuracy higher than training)")
else:
    print("✓ Model generalizes well (no significant overfitting)")

#  EXTRA: Try different model architectures 
print("\n" + "="*60)
print("EXTRA: SIMPLER MODEL FOR COMPARISON")
print("="*60)

# Create a simpler CNN model
simple_model = Sequential([
    layers.Conv2D(16, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

simple_model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("Simple model architecture:")
simple_model.summary()

# Train for fewer epochs
simple_history = simple_model.fit(
    X_train, y_train,
    batch_size=64,
    epochs=8,
    validation_data=(X_val, y_val),
    verbose=0
)

simple_test_loss, simple_test_acc = simple_model.evaluate(X_test_cnn, y_test_encoded, verbose=0)

print(f"\nSimple Model Test Accuracy: {simple_test_acc:.4f}")
print(f"Complex Model Test Accuracy: {test_accuracy:.4f}")
print(f"Improvement: {(test_accuracy - simple_test_acc):+.4f}")