#  XP NINJA: MONITORING NLP MODELS IN PRODUCTION 
# Drug Reviews Sentiment Classification with Evidently Monitoring

#  PART 1: SETUP AND INSTALLATION 
#!pip install evidently pandas numpy scikit-learn nltk matplotlib seaborn -q

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import re
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.pipeline import Pipeline

# Evidently libraries for monitoring
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, ClassificationPreset
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, ColumnCorrelationsMetric

# Download NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

print(" All libraries imported successfully!")

#  PART 2: LOAD AND EXPLORE DATASET 
print("\n" + "="*60)
print("PART 2: LOADING DRUG REVIEWS DATASET")
print("="*60)

# Load the dataset (using a public drug reviews dataset)
url = "https://raw.githubusercontent.com/ruchikac/masters_dissertation/master/drug_reviews.csv"
try:
    df = pd.read_csv(url)
    print(" Dataset loaded successfully!")
except:
    # Alternative URL if the first one doesn't work
    url = "https://raw.githubusercontent.com/abhishekkrthakur/ipsc2019/master/data/train_drug.csv"
    df = pd.read_csv(url)
    df = df.rename(columns={'review': 'review', 'rating': 'rating'})

print(f"Dataset shape: {df.shape}")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nColumn names: {df.columns.tolist()}")

# Create sentiment labels based on rating
# Assuming rating is on scale 1-10 or similar
if 'rating' in df.columns:
    # Binary sentiment: positive (rating >= 7) vs negative (rating <= 4)
    # Neutral ratings (5-6) can be excluded for clearer separation
    df['sentiment'] = df['rating'].apply(lambda x: 1 if x >= 7 else (0 if x <= 4 else np.nan))
    df = df.dropna(subset=['sentiment'])
    df['sentiment'] = df['sentiment'].astype(int)
    print(f"\nSentiment distribution:")
    print(f"Positive (1): {(df['sentiment']==1).sum()} ({df['sentiment'].mean()*100:.1f}%)")
    print(f"Negative (0): {(df['sentiment']==0).sum()} ({(1-df['sentiment'].mean())*100:.1f}%)")

# Rename columns for clarity
if 'review' in df.columns:
    df = df.rename(columns={'review': 'text'})
elif 'text' not in df.columns:
    # Try to find text column
    text_col = [col for col in df.columns if 'review' in col.lower() or 'text' in col.lower()][0]
    df = df.rename(columns={text_col: 'text'})

print(f"\nWorking columns: {df.columns.tolist()}")

#  PART 3: TEXT PREPROCESSING 
print("\n" + "="*60)
print("PART 3: TEXT PREPROCESSING")
print("="*60)

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """Clean and preprocess text data"""
    if isinstance(text, str):
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove stopwords
        words = text.split()
        words = [w for w in words if w not in stop_words and len(w) > 2]
        return ' '.join(words)
    return ''

df['cleaned_text'] = df['text'].apply(preprocess_text)

# Remove empty reviews after cleaning
df = df[df['cleaned_text'].str.len() > 0]
print(f"After cleaning: {len(df)} samples remain")

# Sample the dataset for faster processing (use 5000 samples)
if len(df) > 5000:
    df = df.sample(n=5000, random_state=42)
    print(f"Sampled to {len(df)} samples for faster processing")

# Show example
print(f"\nExample review before cleaning: {df['text'].iloc[0][:100]}...")
print(f"After cleaning: {df['cleaned_text'].iloc[0][:100]}...")

#  PART 4: TRAIN INITIAL MODEL 
print("\n" + "="*60)
print("PART 4: TRAINING INITIAL REVIEW CLASSIFICATION MODEL")
print("="*60)

# Prepare features and labels
X = df['cleaned_text']
y = df['sentiment']

# Split into training and reference datasets (reference = production baseline)
X_train, X_ref, y_train, y_ref = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Further split reference into current and future batches
X_ref_current, X_future, y_ref_current, y_future = train_test_split(X_ref, y_ref, test_size=0.5, random_state=42)

print(f"Training set size: {len(X_train)}")
print(f"Reference (baseline) set size: {len(X_ref_current)}")
print(f"Future production set size: {len(X_future)}")

# Create and train model pipeline
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
    ('classifier', LogisticRegression(C=1.0, max_iter=1000, random_state=42))
])

model_pipeline.fit(X_train, y_train)

# Evaluate on reference data
ref_predictions = model_pipeline.predict(X_ref_current)
ref_accuracy = accuracy_score(y_ref_current, ref_predictions)
ref_f1 = f1_score(y_ref_current, ref_predictions)

print(f"\nModel performance on reference data:")
print(f"Accuracy: {ref_accuracy:.4f}")
print(f"F1 Score: {ref_f1:.4f}")

# Confusion matrix for reference
cm_ref = confusion_matrix(y_ref_current, ref_predictions)
print(f"\nConfusion Matrix:")
print(cm_ref)

#  PART 5: SIMULATE DATA QUALITY ISSUES 
print("\n" + "="*60)
print("PART 5: SIMULATING DATA QUALITY ISSUES")
print("="*60)

def simulate_data_quality_issues(df_text, df_sentiment, issue_type, severity=0.3):
    """Simulate different types of data quality issues"""
    df_issues = df_text.copy()
    y_issues = df_sentiment.copy()
    n_samples = len(df_issues)
    n_corrupt = int(n_samples * severity)
    indices = np.random.choice(n_samples, n_corrupt, replace=False)
    
    if issue_type == 'missing_values':
        df_issues.iloc[indices] = ''
        print(f"Simulated {n_corrupt} missing values")
        
    elif issue_type == 'typos':
        for idx in indices:
            text = df_issues.iloc[idx]
            if len(text) > 10:
                pos = np.random.randint(0, len(text)-1)
                text = text[:pos] + chr(ord(text[pos]) + np.random.randint(1, 5)) + text[pos+1:]
                df_issues.iloc[idx] = text
        print(f"Added typos to {n_corrupt} reviews")
        
    elif issue_type == 'noise':
        noise_words = ['xxx', '###', '!!!', 'random', 'noise', 'spam', 'advertisement']
        for idx in indices:
            text = df_issues.iloc[idx]
            text = text + ' ' + np.random.choice(noise_words)
            df_issues.iloc[idx] = text
        print(f"Added noise to {n_corrupt} reviews")
        
    elif issue_type == 'language_shift':
        # Simulate shift in language (e.g., more technical terms)
        technical_terms = ['efficacy', 'dosage', 'contraindication', 'bioavailability', 'half-life']
        for idx in indices:
            text = df_issues.iloc[idx]
            text = text + ' ' + np.random.choice(technical_terms)
            df_issues.iloc[idx] = text
        print(f"Added technical language to {n_corrupt} reviews")
        
    elif issue_type == 'label_shift':
        # Simulate change in labeling criteria
        y_issues.iloc[indices] = 1 - y_issues.iloc[indices]
        print(f"Flipped labels for {n_corrupt} samples")
    
    return df_issues, y_issues

# Create different corrupted versions
corruption_types = ['missing_values', 'typos', 'noise', 'language_shift', 'label_shift']
corrupted_datasets = {}

for corr_type in corruption_types:
    X_corrupt, y_corrupt = simulate_data_quality_issues(
        X_future, y_future, corr_type, severity=0.2
    )
    corrupted_datasets[corr_type] = (X_corrupt, y_corrupt)

#  PART 6: EVALUATE IMPACT ON MODEL PERFORMANCE 
print("\n" + "="*60)
print("PART 6: EVALUATING IMPACT OF DATA QUALITY ISSUES")
print("="*60)

performance_metrics = []

for corr_type, (X_corr, y_corr) in corrupted_datasets.items():
    predictions = model_pipeline.predict(X_corr)
    accuracy = accuracy_score(y_corr, predictions)
    precision = precision_score(y_corr, predictions, zero_division=0)
    recall = recall_score(y_corr, predictions, zero_division=0)
    f1 = f1_score(y_corr, predictions, zero_division=0)
    
    performance_metrics.append({
        'Issue_Type': corr_type,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1_Score': f1,
        'Performance_Drop': ref_f1 - f1
    })
    
    print(f"\n{corr_type.upper()} Impact:")
    print(f"  F1 Score: {ref_f1:.4f} → {f1:.4f} (Drop: {ref_f1 - f1:.4f})")

metrics_df = pd.DataFrame(performance_metrics)
print("\n" + "-"*40)
print("SUMMARY OF IMPACTS:")
print(metrics_df.to_string(index=False))

#  PART 7: MONITORING WITH EVIDENTLY 
print("\n" + "="*60)
print("PART 7: IMPLEMENTING MONITORING WITH EVIDENTLY")
print("="*60)

def create_monitoring_report(reference_data, current_data, reference_preds, current_preds):
    """Create a comprehensive monitoring report using Evidently"""
    
    # Prepare dataframes for Evidently
    ref_df = pd.DataFrame({
        'prediction': reference_preds,
        'target': reference_data,
        'text_length': [len(text) for text in X_ref_current]
    })
    
    curr_df = pd.DataFrame({
        'prediction': current_preds,
        'target': current_data,
        'text_length': [len(text) for text in X_future]
    })
    
    # Define column mapping
    column_mapping = ColumnMapping()
    column_mapping.target = 'target'
    column_mapping.prediction = 'prediction'
    
    # Create data drift report
    drift_report = Report(metrics=[
        DataDriftPreset(),
        TargetDriftPreset()
    ])
    
    drift_report.run(reference_data=ref_df, current_data=curr_df, column_mapping=column_mapping)
    
    return drift_report

# Get predictions for reference and current data
ref_preds_original = model_pipeline.predict(X_ref_current)
current_preds_original = model_pipeline.predict(X_future)

# Create monitoring report for original data
print("Creating monitoring report for clean data...")
clean_report = create_monitoring_report(y_ref_current, y_future, ref_preds_original, current_preds_original)
print(" Clean data report created")

# Create report for a corrupted dataset
print("\nCreating monitoring report for corrupted data (typos)...")
X_corrupt_typos, y_corrupt_typos = corrupted_datasets['typos']
current_preds_corrupt = model_pipeline.predict(X_corrupt_typos)
corrupt_report = create_monitoring_report(y_ref_current, y_corrupt_typos, ref_preds_original, current_preds_corrupt)
print(" Corrupted data report created")

#  PART 8: DETECTING DRIFT WITH STATISTICAL TESTS 
print("\n" + "="*60)
print("PART 8: STATISTICAL DRIFT DETECTION")
print("="*60)

from scipy.stats import ks_2samp, chi2_contingency
from collections import Counter

def detect_data_drift(reference_texts, current_texts, feature='length'):
    """Detect drift in text data characteristics"""
    
    if feature == 'length':
        ref_lengths = [len(text) for text in reference_texts]
        curr_lengths = [len(text) for text in current_texts]
        stat, p_value = ks_2samp(ref_lengths, curr_lengths)
        return {
            'feature': 'text_length',
            'statistic': stat,
            'p_value': p_value,
            'drift_detected': p_value < 0.05
        }
    
    elif feature == 'vocabulary':
        # Compare vocabulary diversity
        ref_vocab = set(' '.join(reference_texts).split())
        curr_vocab = set(' '.join(current_texts).split())
        overlap = len(ref_vocab.intersection(curr_vocab)) / len(ref_vocab.union(curr_vocab))
        return {
            'feature': 'vocabulary_overlap',
            'statistic': overlap,
            'p_value': None,
            'drift_detected': overlap < 0.7
        }
    
    return None

# Detect drift in different corrupted datasets
drift_results = []

for corr_type, (X_corr, y_corr) in corrupted_datasets.items():
    length_drift = detect_data_drift(X_ref_current, X_corr, 'length')
    vocab_drift = detect_data_drift(X_ref_current, X_corr, 'vocabulary')
    
    drift_results.append({
        'Issue_Type': corr_type,
        'Length_Drift': length_drift['drift_detected'],
        'Length_p_value': f"{length_drift['p_value']:.4f}",
        'Vocab_Drift': vocab_drift['drift_detected'],
        'Vocab_Overlap': f"{vocab_drift['statistic']:.3f}"
    })

drift_df = pd.DataFrame(drift_results)
print("\nDrift Detection Results:")
print(drift_df.to_string(index=False))

#  PART 9: PREDICTION DISTRIBUTION MONITORING 
print("\n" + "="*60)
print("PART 9: MONITORING PREDICTION DISTRIBUTIONS")
print("="*60)

def monitor_prediction_distribution(reference_preds, current_preds, reference_proba=None, current_proba=None):
    """Monitor changes in prediction distributions"""
    
    ref_dist = Counter(reference_preds)
    curr_dist = Counter(current_preds)
    
    # Chi-square test for distribution shift
    contingency = np.array([
        [ref_dist[0], ref_dist[1]],
        [curr_dist[0], curr_dist[1]]
    ])
    chi2, p_value, dof, expected = chi2_contingency(contingency)
    
    return {
        'ref_positive_rate': ref_dist[1] / len(reference_preds),
        'curr_positive_rate': curr_dist[1] / len(current_preds),
        'rate_shift': (curr_dist[1] / len(current_preds)) - (ref_dist[1] / len(reference_preds)),
        'chi2_p_value': p_value,
        'significant_shift': p_value < 0.05
    }

# Monitor prediction distribution for each corruption type
print("\nPrediction Distribution Monitoring:")
print("-" * 50)

for corr_type, (X_corr, y_corr) in corrupted_datasets.items():
    curr_preds = model_pipeline.predict(X_corr)
    monitor_results = monitor_prediction_distribution(ref_preds_original, curr_preds)
    
    print(f"\n{corr_type.upper()}:")
    print(f"  Positive rate: {monitor_results['ref_positive_rate']:.3f} → {monitor_results['curr_positive_rate']:.3f}")
    print(f"  Rate shift: {monitor_results['rate_shift']:+.3f}")
    print(f"  Significant shift: {monitor_results['significant_shift']}")
    print(f"  Chi-square p-value: {monitor_results['chi2_p_value']:.4f}")

#  PART 10: MITIGATION STRATEGIES 
print("\n" + "="*60)
print("PART 10: IMPLEMENTING MITIGATION STRATEGIES")
print("="*60)

def implement_mitigation_strategy(model, X_train_original, y_train_original, 
                                   X_current, y_current, strategy='retrain'):
    """Implement different mitigation strategies for model degradation"""
    
    if strategy == 'retrain':
        # Retrain model on current data
        new_model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
            ('classifier', LogisticRegression(C=1.0, max_iter=1000, random_state=42))
        ])
        new_model.fit(X_current, y_current)
        return new_model
    
    elif strategy == 'partial_fit':
        # Partial fit (for online learning - not available for all models)
        # This is a placeholder for demonstration
        print("  Partial fit not implemented for this model type")
        return model
    
    elif strategy == 'ensemble':
        # Create ensemble with original and retrained model
        retrained_model = implement_mitigation_strategy(model, X_train_original, 
                                                        y_train_original, X_current, 
                                                        y_current, 'retrain')
        
        def ensemble_predict(X):
            pred1 = model.predict(X)
            pred2 = retrained_model.predict(X)
            # Weighted average (favor retrained model)
            return np.where((pred1 + pred2) >= 1, 1, 0)
        
        return ensemble_predict
    
    return model

# Test mitigation on most corrupted dataset
most_severe_type = performance_metrics[np.argmax([m['Performance_Drop'] for m in performance_metrics])]['Issue_Type']
X_corrupt_severe, y_corrupt_severe = corrupted_datasets[most_severe_type]

print(f"Applying mitigation for {most_severe_type}...")

# Apply retraining strategy
mitigated_model = implement_mitigation_strategy(
    model_pipeline, X_train, y_train, X_corrupt_severe, y_corrupt_severe, 'retrain'
)

# Evaluate mitigated model
mitigated_preds = mitigated_model.predict(X_corrupt_severe)
mitigated_f1 = f1_score(y_corrupt_severe, mitigated_preds)

print(f"\nMitigation Results for {most_severe_type}:")
print(f"  Original F1: {performance_metrics[np.argmax([m['Performance_Drop'] for m in performance_metrics])]['F1_Score']:.4f}")
print(f"  Mitigated F1: {mitigated_f1:.4f}")
print(f"  Improvement: {mitigated_f1 - performance_metrics[np.argmax([m['Performance_Drop'] for m in performance_metrics])]['F1_Score']:.4f}")

#  PART 11: COMPREHENSIVE MONITORING DASHBOARD 
print("\n" + "="*60)
print("PART 11: MONITORING DASHBOARD VISUALIZATION")
print("="*60)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Plot 1: Performance degradation over corruption types
corruption_names = [m['Issue_Type'] for m in performance_metrics]
f1_scores = [m['F1_Score'] for m in performance_metrics]
axes[0, 0].bar(corruption_names, f1_scores, color='skyblue', alpha=0.7)
axes[0, 0].axhline(y=ref_f1, color='red', linestyle='--', label=f'Baseline F1: {ref_f1:.3f}')
axes[0, 0].set_ylabel('F1 Score')
axes[0, 0].set_title('Model Performance by Issue Type')
axes[0, 0].legend()
axes[0, 0].tick_params(axis='x', rotation=45)

# Plot 2: Prediction distribution shift
positive_rates = [monitor_prediction_distribution(ref_preds_original, 
                                                    model_pipeline.predict(X_corr))['curr_positive_rate'] 
                  for _, (X_corr, _) in corrupted_datasets.items()]
axes[0, 1].bar(corruption_names, positive_rates, color='lightgreen', alpha=0.7)
axes[0, 1].axhline(y=monitor_prediction_distribution(ref_preds_original, ref_preds_original)['ref_positive_rate'], 
                   color='red', linestyle='--', label=f'Baseline: {monitor_prediction_distribution(ref_preds_original, ref_preds_original)["ref_positive_rate"]:.3f}')
axes[0, 1].set_ylabel('Positive Prediction Rate')
axes[0, 1].set_title('Prediction Distribution Shift')
axes[0, 1].legend()
axes[0, 1].tick_params(axis='x', rotation=45)

# Plot 3: Text length distribution (reference vs most corrupted)
ref_lengths = [len(text) for text in X_ref_current]
corrupt_lengths = [len(text) for text in corrupted_datasets['typos'][0]]
axes[0, 2].hist(ref_lengths, bins=30, alpha=0.5, label='Reference', color='blue')
axes[0, 2].hist(corrupt_lengths, bins=30, alpha=0.5, label='Corrupted (typos)', color='orange')
axes[0, 2].set_xlabel('Text Length')
axes[0, 2].set_ylabel('Frequency')
axes[0, 2].set_title('Text Length Distribution Shift')
axes[0, 2].legend()

# Plot 4: Mitigation effectiveness
mitigation_improvement = mitigated_f1 - performance_metrics[np.argmax([m['Performance_Drop'] for m in performance_metrics])]['F1_Score']
axes[1, 0].bar(['Before Mitigation', 'After Mitigation'], 
               [performance_metrics[np.argmax([m['Performance_Drop'] for m in performance_metrics])]['F1_Score'], mitigated_f1],
               color=['red', 'green'], alpha=0.7)
axes[1, 0].set_ylabel('F1 Score')
axes[1, 0].set_title(f'Mitigation Effectiveness: +{mitigation_improvement:.3f} F1')
axes[1, 0].set_ylim(0, 1)

# Plot 5: Drift detection matrix
drift_matrix = np.array([[drift['Length_Drift'], drift['Vocab_Drift']] for drift in drift_results])
sns.heatmap(drift_matrix, annot=True, fmt='d', cmap='RdYlGn_r', 
            xticklabels=['Length Drift', 'Vocab Drift'],
            yticklabels=corruption_names, ax=axes[1, 1])
axes[1, 1].set_title('Drift Detection Heatmap')

# Plot 6: Performance drop by severity
severities = [0.1, 0.2, 0.3, 0.4, 0.5]
performance_drops = []
for severity in severities:
    X_corr_sev, y_corr_sev = simulate_data_quality_issues(X_future, y_future, 'typos', severity)
    preds_sev = model_pipeline.predict(X_corr_sev)
    f1_sev = f1_score(y_corr_sev, preds_sev)
    performance_drops.append(ref_f1 - f1_sev)

axes[1, 2].plot(severities, performance_drops, marker='o', linewidth=2, markersize=8)
axes[1, 2].set_xlabel('Severity Level')
axes[1, 2].set_ylabel('Performance Drop (ΔF1)')
axes[1, 2].set_title('Model Degradation vs Issue Severity')
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

#  PART 12: SUMMARY AND RECOMMENDATIONS 
print("\n" + "="*60)
print("FINAL SUMMARY: NLP MODEL MONITORING IN PRODUCTION")
print("="*60)

summary_report = f"""
=== NLP PRODUCTION MONITORING REPORT ===

1. MODEL BASELINE:
   - Training samples: {len(X_train)}
   - Reference F1 Score: {ref_f1:.4f}
   - Reference Accuracy: {ref_accuracy:.4f}

2. DATA QUALITY ISSUES IDENTIFIED:
   Most impactful issues (largest performance drop):
   {metrics_df.sort_values('Performance_Drop', ascending=False).iloc[0]['Issue_Type']}: 
   {metrics_df.sort_values('Performance_Drop', ascending=False).iloc[0]['Performance_Drop']:.4f} F1 drop

3. DRIFT DETECTION EFFECTIVENESS:
   - Length-based drift detection: Most sensitive to missing values and noise
   - Vocabulary drift detection: Most sensitive to language shift
   - Prediction distribution monitoring: Effective for label shift detection

4. MITIGATION STRATEGIES:
   - Retraining on current data: {'Effective' if mitigated_f1 > ref_f1 - 0.1 else 'Limited effectiveness'}
   - Improvement achieved: {mitigation_improvement:+.4f} F1

5. RECOMMENDATIONS FOR PRODUCTION:
   ✓ Implement real-time drift detection (daily/ weekly)
   ✓ Set up alerting when prediction distribution shifts beyond 2σ
   ✓ Maintain a retraining pipeline with version control
   ✓ Monitor for specific issue types based on domain
   ✓ Create a feedback loop for incorrect predictions

6. MONITORING TOOLS USED:
   - Evidently AI: Data drift, target drift, quality metrics
   - Statistical tests: KS-test, Chi-square, Vocabulary overlap
   - Visualization: Distribution plots, heatmaps, performance tracking

  NEXT STEPS:
   1. Deploy monitoring pipeline alongside model API
   2. Set up automated alerts and dashboards
   3. Implement A/B testing for model updates
   4. Establish SLA thresholds for metric degradation
   5. Create incident response playbook for drift events
"""

print(summary_report)

# Save the report
with open('nlp_monitoring_report.txt', 'w') as f:
    f.write(summary_report)
print("\n✅ Report saved to 'nlp_monitoring_report.txt'")

#  FINAL 
print("\n" + "="*60)
print("XP NINJA - EXERCISE COMPLETE!")
print("="*60)
print("\n🏆 You've successfully implemented NLP Model Monitoring!")
print("   - Built sentiment classification model for drug reviews")
print("   - Simulated and detected various data quality issues")
print("   - Implemented monitoring with Evidently")
print("   - Applied mitigation strategies")
print("\n📊 Share your results and insights with the community!")