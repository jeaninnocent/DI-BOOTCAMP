"""
Classification Metrics and Model Evaluation Toolkit
Includes:
- Calculation of Accuracy, Precision, Recall, F1 from confusion matrix
- Discussion of trade-offs, class imbalance, threshold tuning
- Cross-validation and learning curves
- ROC/AUC for optimal threshold selection

Run this script to see outputs for all exercises.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, roc_curve, auc, roc_auc_score
from sklearn.model_selection import KFold, StratifiedKFold, learning_curve
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.utils import shuffle

# -------------------------------
# Exercise 1: Analyzing Confusion Matrix
# -------------------------------
def exercise1_spam_example():
    print("\n" + "="*60)
    print("EXERCISE 1: Confusion Matrix for Spam Detection")
    print("="*60)
    
    # Definitions in context of email spam detection
    print("\n1.1 Definitions (Spam vs Not Spam):")
    print("- True Positive (TP): Email correctly classified as Spam (actual Spam, predicted Spam)")
    print("- True Negative (TN): Email correctly classified as Not Spam (actual Not Spam, predicted Not Spam)")
    print("- False Positive (FP): Email incorrectly classified as Spam (actual Not Spam, predicted Spam) -> 'false alarm'")
    print("- False Negative (FN): Email incorrectly classified as Not Spam (actual Spam, predicted Not Spam) -> 'missed spam'")
    
    # Given confusion matrix values (example)
    TP, TN, FP, FN = 85, 910, 30, 15   # total 1040 emails
    
    # Calculate metrics
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if (TP+FP) > 0 else 0
    recall = TP / (TP + FN) if (TP+FN) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision+recall) > 0 else 0
    
    print(f"\n1.2 Metrics from confusion matrix (TP={TP}, TN={TN}, FP={FP}, FN={FN}):")
    print(f"Accuracy  = {accuracy:.3f}")
    print(f"Precision = {precision:.3f}")
    print(f"Recall    = {recall:.3f}")
    print(f"F1-Score  = {f1:.3f}")
    
    # Discussion on FP vs FN
    print("\n1.3 Impact of more False Positives vs False Negatives:")
    print("- More FP: Many legitimate emails go to spam folder -> user frustration, missed important messages.")
    print("- More FN: Many spam emails reach inbox -> security risk, time wasted deleting spam.")
    print("Trade-off depends on cost: FP costly for user trust, FN costly for security.")
    
    return {"TP":TP,"TN":TN,"FP":FP,"FN":FN,"accuracy":accuracy,"precision":precision,"recall":recall,"f1":f1}

# -------------------------------
# Exercise 2: Trade-offs in Metrics
# -------------------------------
def exercise2_medical_tradeoffs():
    print("\n" + "="*60)
    print("EXERCISE 2: Medical Diagnosis – Recall vs Precision")
    print("="*60)
    
    print("\n2.1 Why recall > precision in disease screening?")
    print("- Recall = ability to find ALL patients with disease (low FN). Missing a diseased patient (FN) can be fatal.")
    print("- High recall ensures few false negatives. Precision matters less because further tests can rule out false positives.")
    
    print("\n2.2 Scenario where precision > recall:")
    print("Predicting fraud in credit card transactions. A false positive (flagging legitimate transaction as fraud)")
    print("annoys customers and blocks sales. False negatives (missing actual fraud) are costly but less frequent.")
    print("Thus high precision (few false alarms) is prioritized.")
    
    print("\n2.3 Consequences of focusing solely on accuracy in imbalanced datasets:")
    print("- In a dataset with 95% healthy, 5% diseased, a model predicting 'healthy' always gives 95% accuracy")
    print("but fails to detect any disease (recall=0). Accuracy is misleading; need precision/recall or F1.")
    
    return

# -------------------------------
# Exercise 3: Cross-Validation & Learning Curves
# -------------------------------
def exercise3_cv_and_learning_curves():
    print("\n" + "="*60)
    print("EXERCISE 3: Cross-Validation and Learning Curves")
    print("="*60)
    
    # 3.1 K-Fold vs Stratified K-Fold
    print("\n3.1 Difference between K-Fold and Stratified K-Fold:")
    print("- K-Fold: splits data into k folds randomly. Class distribution may vary across folds.")
    print("- Stratified K-Fold: preserves percentage of each class in each fold.")
    print("For housing price prediction (regression), class imbalance is not a typical issue,")
    print("so standard K-Fold is fine. If target is binned (e.g., cheap/expensive), use Stratified.")
    
    # Demonstration of folds on a small dataset
    X = np.random.rand(20, 5)
    y = np.array([0]*15 + [1]*5)  # imbalanced binary
    print("\nExample: 20 samples (15 class0, 5 class1)")
    print("KFold(5):")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    for i, (train_idx, val_idx) in enumerate(kf.split(X)):
        print(f"  Fold {i+1}: train size={len(train_idx)}, val size={len(val_idx)} | val class1 count = {y[val_idx].sum()}")
    print("StratifiedKFold(5):")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for i, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        print(f"  Fold {i+1}: train size={len(train_idx)}, val size={len(val_idx)} | val class1 count = {y[val_idx].sum()}")
    
    # 3.2 Learning curves
    print("\n3.2 What are learning curves?")
    print("Learning curves plot training and validation scores as function of training set size.")
    print("They help diagnose bias/variance, overfitting, and whether more data would help.")
    
    # Generate synthetic regression data for learning curve demo
    X_reg, y_reg = make_classification(n_samples=300, n_features=2, n_redundant=0, 
                                       n_clusters_per_class=1, random_state=42)
    model = LogisticRegression()
    train_sizes, train_scores, test_scores = learning_curve(
        model, X_reg, y_reg, cv=5, train_sizes=np.linspace(0.1, 1.0, 5),
        scoring='accuracy', random_state=42)
    
    train_mean = np.mean(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    
    plt.figure(figsize=(8,5))
    plt.plot(train_sizes, train_mean, 'o-', label='Training score')
    plt.plot(train_sizes, test_mean, 'o-', label='Cross-validation score')
    plt.xlabel('Training examples')
    plt.ylabel('Accuracy')
    plt.title('Learning Curve Example')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('learning_curve_example.png')
    print("\nLearning curve plot saved as 'learning_curve_example.png'")
    
    # 3.3 Underfitting / Overfitting from learning curves
    print("\n3.3 Implications of underfitting and overfitting:")
    print("- Underfitting: Both training and validation scores low, curves plateau close together.")
    print("  Solutions: increase model complexity, add features, reduce regularization.")
    print("- Overfitting: Training score high, validation score significantly lower (gap).")
    print("  Solutions: get more data, reduce model complexity, add regularization, early stopping.")
    
    return

# -------------------------------
# Exercise 4: Class Imbalance Impact
# -------------------------------
def exercise4_rare_disease():
    print("\n" + "="*60)
    print("EXERCISE 4: Class Imbalance – Rare Disease (2% positive)")
    print("="*60)
    
    # 4.1 Accuracy misleading
    print("\n4.1 Why accuracy is misleading:")
    print("If 2% have disease, a model that always predicts 'no disease' gets 98% accuracy")
    print("but is useless (recall=0). Accuracy ignores the minority class completely.")
    
    # 4.2 Importance of precision/recall
    print("\n4.2 Importance of precision and recall:")
    print("- Recall (sensitivity): fraction of actual diseased correctly detected. Critical to avoid false negatives.")
    print("- Precision: fraction of predicted diseased that are truly diseased. Low precision means many false alarms, costly for follow-up.")
    print("F1-score balances both.")
    
    # 4.3 Strategies to handle imbalance
    print("\n4.3 Strategies to evaluate/improve model:")
    print("Evaluation: Use precision, recall, F1, ROC-AUC, PR curve (Precision-Recall).")
    print("Improvement techniques:")
    print("   - Resampling: Oversample minority class (SMOTE) or undersample majority class.")
    print("   - Class weights: Assign higher penalty to misclassifying minority class (e.g., 'balanced' in sklearn).")
    print("   - Use anomaly detection algorithms (Isolation Forest, One-Class SVM).")
    print("   - Collect more data for minority class if possible.")
    print("   - Use appropriate metrics and threshold tuning (see Exercise 5).")
    
    return

# -------------------------------
# Exercise 5: Threshold Tuning with ROC/AUC
# -------------------------------
def exercise5_threshold_tuning():
    print("\n" + "="*60)
    print("EXERCISE 5: Threshold Tuning for Loan Default Prediction")
    print("="*60)
    
    # Create synthetic dataset for demonstration
    X, y = make_classification(n_samples=1000, n_features=10, n_informative=8, 
                               n_redundant=2, weights=[0.9, 0.1], random_state=42)
    X_train, y_train = X[:800], y[:800]
    X_test, y_test = X[800:], y[800:]
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # 5.1 Effect of changing threshold
    print("\n5.1 Changing threshold from 0.5 to 0.7:")
    thresh_05 = 0.5
    thresh_07 = 0.7
    y_pred_05 = (y_proba >= thresh_05).astype(int)
    y_pred_07 = (y_proba >= thresh_07).astype(int)
    
    prec_05 = precision_score(y_test, y_pred_05, zero_division=0)
    rec_05 = recall_score(y_test, y_pred_05)
    prec_07 = precision_score(y_test, y_pred_07, zero_division=0)
    rec_07 = recall_score(y_test, y_pred_07)
    
    print(f"Threshold 0.5 -> Precision={prec_05:.3f}, Recall={rec_05:.3f}")
    print(f"Threshold 0.7 -> Precision={prec_07:.3f}, Recall={rec_07:.3f}")
    print("Increasing threshold makes model more conservative (fewer positives):")
    print("  - Precision increases (fewer false positives)")
    print("  - Recall decreases (more false negatives)")
    
    # 5.2 Consequences of too high / too low threshold
    print("\n5.2 Consequences for loan default prediction:")
    print("- Threshold too high (e.g., 0.9): Very few clients flagged as default -> many actual defaulters missed (high FN).")
    print("  Bank loses money from unrecovered loans.")
    print("- Threshold too low (e.g., 0.1): Many clients flagged as default -> many false positives (low precision).")
    print("  Bank rejects good customers, loses business, damages reputation.")
    
    # 5.3 ROC/AUC for optimal threshold
    fpr, tpr, thresholds = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    
    # Find threshold that maximizes Youden's J = tpr - fpr
    youden = tpr - fpr
    best_idx = np.argmax(youden)
    best_thresh = thresholds[best_idx]
    
    plt.figure(figsize=(8,6))
    plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0,1], [0,1], 'k--', label='Random')
    plt.scatter(fpr[best_idx], tpr[best_idx], color='red', label=f'Best threshold = {best_thresh:.3f}')
    plt.xlabel('False Positive Rate (1 - Specificity)')
    plt.ylabel('True Positive Rate (Recall)')
    plt.title('ROC Curve for Threshold Selection')
    plt.legend()
    plt.grid(True)
    plt.savefig('roc_curve_example.png')
    print(f"\nROC curve saved as 'roc_curve_example.png'")
    print(f"AUC = {roc_auc:.3f} (higher = better separation)")
    print(f"Optimal threshold (Youden's index) ≈ {best_thresh:.3f}")
    print("\nROC curves show trade-off between TPR (recall) and FPR. AUC summarizes overall performance.")
    print("Choose threshold based on business cost: for loan default, you might prefer a threshold that")
    print("minimizes total cost = cost_FN * FN_rate + cost_FP * FP_rate.")
    
    return

# -------------------------------
# Framework: Evaluation for classification models
# -------------------------------
class ModelEvaluationFramework:
    """
    Framework for evaluating classification models, with special focus on
    class imbalance and threshold tuning.
    """
    
    def __init__(self, model, X, y, positive_class=1):
        self.model = model
        self.X = X
        self.y = y
        self.positive = positive_class
        
    def evaluate_threshold_range(self, thresholds=np.linspace(0.1, 0.9, 9)):
        """Compute precision, recall, F1 for multiple thresholds."""
        y_proba = self.model.predict_proba(self.X)[:, 1]
        results = []
        for thresh in thresholds:
            y_pred = (y_proba >= thresh).astype(int)
            prec = precision_score(self.y, y_pred, pos_label=self.positive, zero_division=0)
            rec = recall_score(self.y, y_pred, pos_label=self.positive)
            f1 = f1_score(self.y, y_pred, pos_label=self.positive)
            results.append((thresh, prec, rec, f1))
        return results
    
    def print_best_threshold_by_metric(self, metric='f1'):
        """Find threshold that maximizes chosen metric."""
        y_proba = self.model.predict_proba(self.X)[:, 1]
        best_score = -1
        best_thresh = 0.5
        for thresh in np.linspace(0.01, 0.99, 100):
            y_pred = (y_proba >= thresh).astype(int)
            if metric == 'f1':
                score = f1_score(self.y, y_pred, pos_label=self.positive)
            elif metric == 'precision':
                score = precision_score(self.y, y_pred, pos_label=self.positive, zero_division=0)
            elif metric == 'recall':
                score = recall_score(self.y, y_pred, pos_label=self.positive)
            else:
                raise ValueError("metric must be 'f1', 'precision', or 'recall'")
            if score > best_score:
                best_score = score
                best_thresh = thresh
        print(f"Best threshold for maximizing {metric}: {best_thresh:.3f} (score={best_score:.3f})")
        return best_thresh, best_score

# -------------------------------
# Main execution (runs all exercises)
# -------------------------------
if __name__ == "__main__":
    # Run all exercises sequentially
    exercise1_spam_example()
    exercise2_medical_tradeoffs()
    exercise3_cv_and_learning_curves()
    exercise4_rare_disease()
    exercise5_threshold_tuning()
    
    # Example usage of the evaluation framework
    print("\n" + "="*60)
    print("EVALUATION FRAMEWORK DEMO")
    print("="*60)
    # Generate imbalanced data
    X_imb, y_imb = make_classification(n_samples=500, n_features=5, weights=[0.95, 0.05], random_state=42)
    model = LogisticRegression(class_weight='balanced')  # handle imbalance
    model.fit(X_imb, y_imb)
    framework = ModelEvaluationFramework(model, X_imb, y_imb)
    results = framework.evaluate_threshold_range()
    print("Threshold | Precision | Recall | F1")
    for th, prec, rec, f1 in results:
        print(f"{th:.2f}       | {prec:.3f}      | {rec:.3f}   | {f1:.3f}")
    framework.print_best_threshold_by_metric('f1')
    
    print("\nAll exercises complete. Check generated PNG files for learning curve and ROC curve.")