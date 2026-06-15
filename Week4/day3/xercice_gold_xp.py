import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow as tf
from tensorflow import keras
from scikeras.wrappers import KerasClassifier
import warnings
warnings.filterwarnings('ignore')

#  EXERCISE 1: Exploratory Data Analysis 
print("="*60)
print("EXERCISE 1: Exploratory Data Analysis")
print("="*60)

# Load dataset
titanic_url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(titanic_url)

print(f"Dataset shape: {df.shape}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nDataset info:\n{df.info()}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# Data cleaning
df_clean = df.copy()
df_clean['Age'].fillna(df_clean['Age'].median(), inplace=True)
df_clean['Embarked'].fillna(df_clean['Embarked'].mode()[0], inplace=True)
df_clean.drop('Cabin', axis=1, inplace=True)

# Feature engineering
df_clean['FamilySize'] = df_clean['SibSp'] + df_clean['Parch'] + 1
df_clean['IsAlone'] = (df_clean['FamilySize'] == 1).astype(int)
df_clean['Title'] = df_clean['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
df_clean['Title'] = df_clean['Title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
df_clean['Title'] = df_clean['Title'].replace(['Mlle', 'Ms'], 'Miss')
df_clean['Title'] = df_clean['Title'].replace('Mme', 'Mrs')

# Encode categorical variables
le_sex = LabelEncoder()
le_embarked = LabelEncoder()
le_title = LabelEncoder()

df_clean['Sex'] = le_sex.fit_transform(df_clean['Sex'])
df_clean['Embarked'] = le_embarked.fit_transform(df_clean['Embarked'])
df_clean['Title'] = le_title.fit_transform(df_clean['Title'])

# Select features for modeling
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'FamilySize', 'IsAlone', 'Title']
X = df_clean[features]
y = df_clean['Survived']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nTraining set size: {X_train.shape}")
print(f"Test set size: {X_test.shape}")
print(f"Survival rate in training: {y_train.mean():.2%}")
print(f"Survival rate in test: {y_test.mean():.2%}")

# Visualizations
plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
sns.countplot(data=df_clean, x='Survived', hue='Sex')
plt.title('Survival by Gender')

plt.subplot(2, 3, 2)
sns.countplot(data=df_clean, x='Survived', hue='Pclass')
plt.title('Survival by Passenger Class')

plt.subplot(2, 3, 3)
sns.histplot(data=df_clean, x='Age', hue='Survived', bins=30, alpha=0.6)
plt.title('Age Distribution by Survival')

plt.subplot(2, 3, 4)
sns.countplot(data=df_clean, x='Survived', hue='Embarked')
plt.title('Survival by Embarkation Port')

plt.subplot(2, 3, 5)
sns.boxplot(data=df_clean, x='Survived', y='Fare')
plt.title('Fare Distribution by Survival')

plt.subplot(2, 3, 6)
corr_matrix = df_clean[features + ['Survived']].corr()
sns.heatmap(corr_matrix[['Survived']].sort_values(by='Survived', ascending=False), 
            annot=True, cmap='coolwarm', cbar=False)
plt.title('Feature Correlations with Survival')

plt.tight_layout()
plt.show()

#  EXERCISE 2: Decision Tree without Grid Search 
print("\n" + "="*60)
print("EXERCISE 2: Decision Tree Classifier without Grid Search")
print("="*60)

dt_manual = DecisionTreeClassifier(
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5,
    criterion='gini',
    random_state=42
)

dt_manual.fit(X_train, y_train)
y_pred_dt_manual = dt_manual.predict(X_test)

print("Manual Decision Tree Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_dt_manual):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_dt_manual):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_dt_manual):.4f}")
print(f"F1 Score: {f1_score(y_test, y_pred_dt_manual):.4f}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred_dt_manual)}")

#  EXERCISE 3: Decision Tree with Grid Search 
print("\n" + "="*60)
print("EXERCISE 3: Decision Tree Classifier with Grid Search")
print("="*60)

param_grid_dt = {
    'max_depth': [3, 5, 7, 10, None],
    'min_samples_split': [2, 5, 10, 20],
    'min_samples_leaf': [1, 2, 5, 10],
    'criterion': ['gini', 'entropy']
}

grid_search_dt = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid_dt,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=0
)

grid_search_dt.fit(X_train, y_train)
dt_tuned = grid_search_dt.best_estimator_
y_pred_dt_tuned = dt_tuned.predict(X_test)

print(f"Best parameters: {grid_search_dt.best_params_}")
print(f"Best cross-validation score: {grid_search_dt.best_score_:.4f}\n")

print("Tuned Decision Tree Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_dt_tuned):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_dt_tuned):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_dt_tuned):.4f}")
print(f"F1 Score: {f1_score(y_test, y_pred_dt_tuned):.4f}")

print("\nComparison with manual model:")
print(f"Accuracy improvement: {accuracy_score(y_test, y_pred_dt_tuned) - accuracy_score(y_test, y_pred_dt_manual):+.4f}")
print(f"F1 improvement: {f1_score(y_test, y_pred_dt_tuned) - f1_score(y_test, y_pred_dt_manual):+.4f}")

#  EXERCISE 4: KNN without Grid Search 
print("\n" + "="*60)
print("EXERCISE 4: K-Nearest Neighbors without Grid Search")
print("="*60)

# Scale features for KNN
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn_manual = KNeighborsClassifier(
    n_neighbors=5,
    metric='minkowski',
    p=2,
    weights='uniform'
)

knn_manual.fit(X_train_scaled, y_train)
y_pred_knn_manual = knn_manual.predict(X_test_scaled)

print("Manual KNN Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_knn_manual):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_knn_manual):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_knn_manual):.4f}")
print(f"F1 Score: {f1_score(y_test, y_pred_knn_manual):.4f}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred_knn_manual)}")

#  EXERCISE 5: KNN with Grid Search 
print("\n" + "="*60)
print("EXERCISE 5: K-Nearest Neighbors with Grid Search")
print("="*60)

param_grid_knn = {
    'n_neighbors': [3, 5, 7, 9, 11, 15],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan', 'minkowski'],
    'p': [1, 2]
}

grid_search_knn = GridSearchCV(
    KNeighborsClassifier(),
    param_grid_knn,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=0
)

grid_search_knn.fit(X_train_scaled, y_train)
knn_tuned = grid_search_knn.best_estimator_
y_pred_knn_tuned = knn_tuned.predict(X_test_scaled)

print(f"Best parameters: {grid_search_knn.best_params_}")
print(f"Best cross-validation score: {grid_search_knn.best_score_:.4f}\n")

print("Tuned KNN Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_knn_tuned):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_knn_tuned):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_knn_tuned):.4f}")
print(f"F1 Score: {f1_score(y_test, y_pred_knn_tuned):.4f}")

print("\nComparison with manual model:")
print(f"Accuracy improvement: {accuracy_score(y_test, y_pred_knn_tuned) - accuracy_score(y_test, y_pred_knn_manual):+.4f}")
print(f"F1 improvement: {f1_score(y_test, y_pred_knn_tuned) - f1_score(y_test, y_pred_knn_manual):+.4f}")

#  EXERCISE 6: Neural Network without Hyperparameter Tuning 
print("\n" + "="*60)
print("EXERCISE 6: Neural Network Classifier without Hyperparameter Tuning")
print("="*60)

# Scale features for neural network
scaler_nn = StandardScaler()
X_train_nn = scaler_nn.fit_transform(X_train)
X_test_nn = scaler_nn.transform(X_test)

nn_manual = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train_nn.shape[1],)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

nn_manual.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

history_manual = nn_manual.fit(
    X_train_nn, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

y_pred_nn_manual = (nn_manual.predict(X_test_nn, verbose=0) > 0.5).astype(int)

print("Manual Neural Network Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_nn_manual):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_nn_manual):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_nn_manual):.4f}")
print(f"F1 Score: {f1_score(y_test, y_pred_nn_manual):.4f}")

#  EXERCISE 7: Neural Network with Hyperparameter Tuning 
print("\n" + "="*60)
print("EXERCISE 7: Neural Network with Hyperparameter Tuning (Optional)")
print("="*60)

def create_nn_model(optimizer='adam', neurons_1=64, neurons_2=32, dropout_rate=0.3):
    model = keras.Sequential([
        keras.layers.Dense(neurons_1, activation='relu', input_shape=(X_train_nn.shape[1],)),
        keras.layers.Dropout(dropout_rate),
        keras.layers.Dense(neurons_2, activation='relu'),
        keras.layers.Dropout(dropout_rate),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    return model

model = KerasClassifier(model=create_nn_model, epochs=30, batch_size=32, verbose=0)

param_grid_nn = {
    'model__neurons_1': [32, 64, 128],
    'model__neurons_2': [16, 32, 64],
    'model__dropout_rate': [0.2, 0.3, 0.4],
    'model__optimizer': ['adam', 'rmsprop'],
    'batch_size': [16, 32],
    'epochs': [30]
}

random_search_nn = RandomizedSearchCV(
    model,
    param_grid_nn,
    n_iter=10,
    cv=3,
    scoring='f1',
    n_jobs=1,
    verbose=0,
    random_state=42
)

print("Searching for best hyperparameters (this may take a few minutes)...")
random_search_nn.fit(X_train_nn, y_train)
nn_tuned = random_search_nn.best_estimator_
y_pred_nn_tuned = (nn_tuned.predict(X_test_nn) > 0.5).astype(int)

print(f"\nBest parameters: {random_search_nn.best_params_}")
print(f"Best cross-validation score: {random_search_nn.best_score_:.4f}\n")

print("Tuned Neural Network Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred_nn_tuned):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_nn_tuned):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_nn_tuned):.4f}")
print(f"F1 Score: {f1_score(y_test, y_pred_nn_tuned):.4f}")

print("\nComparison with manual model:")
print(f"Accuracy improvement: {accuracy_score(y_test, y_pred_nn_tuned) - accuracy_score(y_test, y_pred_nn_manual):+.4f}")
print(f"F1 improvement: {f1_score(y_test, y_pred_nn_tuned) - f1_score(y_test, y_pred_nn_manual):+.4f}")

#  FINAL COMPARISON AND VISUALIZATIONS 
print("\n" + "="*60)
print("FINAL MODEL COMPARISON")
print("="*60)

models = ['DT Manual', 'DT Tuned', 'KNN Manual', 'KNN Tuned', 'NN Manual', 'NN Tuned']
accuracies = [
    accuracy_score(y_test, y_pred_dt_manual),
    accuracy_score(y_test, y_pred_dt_tuned),
    accuracy_score(y_test, y_pred_knn_manual),
    accuracy_score(y_test, y_pred_knn_tuned),
    accuracy_score(y_test, y_pred_nn_manual),
    accuracy_score(y_test, y_pred_nn_tuned)
]
f1_scores = [
    f1_score(y_test, y_pred_dt_manual),
    f1_score(y_test, y_pred_dt_tuned),
    f1_score(y_test, y_pred_knn_manual),
    f1_score(y_test, y_pred_knn_tuned),
    f1_score(y_test, y_pred_nn_manual),
    f1_score(y_test, y_pred_nn_tuned)
]

comparison_df = pd.DataFrame({
    'Model': models,
    'Accuracy': accuracies,
    'F1 Score': f1_scores
})

print("\n", comparison_df.to_string(index=False))
print(f"\nBest Model by Accuracy: {models[np.argmax(accuracies)]} ({max(accuracies):.4f})")
print(f"Best Model by F1 Score: {models[np.argmax(f1_scores)]} ({max(f1_scores):.4f})")

# Visualization of results
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
x = np.arange(len(models))
width = 0.35
plt.bar(x - width/2, accuracies, width, label='Accuracy', color='skyblue')
plt.bar(x + width/2, f1_scores, width, label='F1 Score', color='lightcoral')
plt.xlabel('Models')
plt.ylabel('Score')
plt.title('Model Performance Comparison')
plt.xticks(x, models, rotation=45, ha='right')
plt.legend()
plt.ylim(0.6, 0.9)

plt.subplot(1, 2, 2)
improvements = [
    accuracy_score(y_test, y_pred_dt_tuned) - accuracy_score(y_test, y_pred_dt_manual),
    accuracy_score(y_test, y_pred_knn_tuned) - accuracy_score(y_test, y_pred_knn_manual),
    accuracy_score(y_test, y_pred_nn_tuned) - accuracy_score(y_test, y_pred_nn_manual)
]
model_names = ['Decision Tree', 'KNN', 'Neural Network']
colors = ['green' if imp > 0 else 'red' for imp in improvements]
plt.bar(model_names, improvements, color=colors)
plt.xlabel('Model Type')
plt.ylabel('Accuracy Improvement')
plt.title('Hyperparameter Tuning Impact')
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
for i, imp in enumerate(improvements):
    plt.text(i, imp + (0.01 if imp > 0 else -0.02), f'{imp:+.4f}', ha='center')

plt.tight_layout()
plt.show()

# Feature importance for best model
if f1_scores[np.argmax(f1_scores)] == f1_scores[1]:  # If tuned DT is best
    feature_importance = dt_tuned.feature_importances_
    feature_names = features
    
    plt.figure(figsize=(10, 6))
    sorted_idx = np.argsort(feature_importance)[::-1]
    plt.barh(range(len(sorted_idx[:10])), feature_importance[sorted_idx[:10]])
    plt.yticks(range(len(sorted_idx[:10])), [feature_names[i] for i in sorted_idx[:10]])
    plt.xlabel('Feature Importance')
    plt.title('Top 10 Feature Importances - Best Model (Tuned Decision Tree)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()