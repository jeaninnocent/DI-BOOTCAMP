"""
Binary Classification Evaluation from Scratch
- Train Logistic Regression on Breast Cancer dataset
- Implement Accuracy, Precision, Recall, F1-Score using confusion matrix components
- Evaluate and interpret results
"""

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# -------------------------------
# Step 1: Load and prepare dataset
# -------------------------------
print("=" * 60)
print("EXERCISE 1: Evaluation Metrics Implementation from Scratch")
print("=" * 60)

data = load_breast_cancer()
X, y = data.data, data.target   # 0 = malignant, 1 = benign (binary)

print(f"\nDataset: Breast Cancer Wisconsin")
print(f"Samples: {X.shape[0]}, Features: {X.shape[1]}")
print(f"Class distribution: Malignant (0) = {np.sum(y==0)}, Benign (1) = {np.sum(y==1)}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Standardize features for logistic regression
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# -------------------------------
# Step 2: Train Logistic Regression
# -------------------------------
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"\nTraining complete. Test set size: {len(y_test)}")

# -------------------------------
# Step 3: Implement metrics from scratch using confusion matrix components
# -------------------------------
def confusion_matrix_components(y_true, y_pred):
    """Calculate TP, TN, FP, FN from scratch"""
    TP = np.sum((y_true == 1) & (y_pred == 1))
    TN = np.sum((y_true == 0) & (y_pred == 0))
    FP = np.sum((y_true == 0) & (y_pred == 1))
    FN = np.sum((y_true == 1) & (y_pred == 0))
    return TP, TN, FP, FN

def accuracy_from_scratch(y_true, y_pred):
    TP, TN, FP, FN = confusion_matrix_components(y_true, y_pred)
    return (TP + TN) / (TP + TN + FP + FN)

def precision_from_scratch(y_true, y_pred):
    TP, TN, FP, FN = confusion_matrix_components(y_true, y_pred)
    if TP + FP == 0:
        return 0.0
    return TP / (TP + FP)

def recall_from_scratch(y_true, y_pred):
    TP, TN, FP, FN = confusion_matrix_components(y_true, y_pred)
    if TP + FN == 0:
        return 0.0
    return TP / (TP + FN)

def f1_score_from_scratch(y_true, y_pred):
    prec = precision_from_scratch(y_true, y_pred)
    rec = recall_from_scratch(y_true, y_pred)
    if prec + rec == 0:
        return 0.0
    return 2 * (prec * rec) / (prec + rec)

# -------------------------------
# Step 4: Calculate metrics and compare with sklearn
# -------------------------------
TP, TN, FP, FN = confusion_matrix_components(y_test, y_pred)
print(f"\nConfusion Matrix Components:")
print(f"TP (True Positives)  = {TP}")
print(f"TN (True Negatives)  = {TN}")
print(f"FP (False Positives) = {FP}")
print(f"FN (False Negatives) = {FN}")

# Our implementations
acc_scratch = accuracy_from_scratch(y_test, y_pred)
prec_scratch = precision_from_scratch(y_test, y_pred)
rec_scratch = recall_from_scratch(y_test, y_pred)
f1_scratch = f1_score_from_scratch(y_test, y_pred)

# sklearn versions for verification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

acc_sklearn = accuracy_score(y_test, y_pred)
prec_sklearn = precision_score(y_test, y_pred)
rec_sklearn = recall_score(y_test, y_pred)
f1_sklearn = f1_score(y_test, y_pred)

print("\n" + "-" * 40)
print("Evaluation Results (from scratch vs sklearn):")
print("-" * 40)
print(f"Accuracy  : {acc_scratch:.4f} (scratch) | {acc_sklearn:.4f} (sklearn)")
print(f"Precision : {prec_scratch:.4f} (scratch) | {prec_sklearn:.4f} (sklearn)")
print(f"Recall    : {rec_scratch:.4f} (scratch) | {rec_sklearn:.4f} (sklearn)")
print(f"F1-Score  : {f1_scratch:.4f} (scratch) | {f1_sklearn:.4f} (sklearn)")

# -------------------------------
# Step 5: Interpretation
# -------------------------------
print("\n" + "-" * 40)
print("Interpretation:")
print("-" * 40)
print(f"Accuracy = {acc_scratch:.4f} → Model correctly classifies {acc_scratch*100:.1f}% of cases.")
print(f"Precision = {prec_scratch:.4f} → Of all 'benign' predictions, {prec_scratch*100:.1f}% are correct.")
print(f"Recall = {rec_scratch:.4f} → Model detects {rec_scratch*100:.1f}% of actual benign tumors.")
print(f"F1-Score = {f1_scratch:.4f} → Harmonic mean of precision and recall.")

# Additional insight: class imbalance check
print(f"\nDataset has {np.sum(y==1)/len(y)*100:.1f}% benign, {np.sum(y==0)/len(y)*100:.1f}% malignant.")
print("All metrics are high, indicating good performance. No severe class imbalance issue.")
print("Note: In medical diagnosis, recall would be critical (avoid false negatives). Here recall is excellent.")

# Optional: Show confusion matrix visually
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=['Malignant', 'Benign'], cmap='Blues')
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig('confusion_matrix_breast_cancer.png')
print("\nConfusion matrix saved as 'confusion_matrix_breast_cancer.png'")