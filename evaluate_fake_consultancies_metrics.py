import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import learning_curve
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
# Configuration
DATA_PATH = "data/consultancies_dataset.csv"
MODEL_PATH = "models/fake_consultancy_research.pkl"
RANDOM_STATE = 42
TEST_SIZE = 0.2

print(f"Loading data from {DATA_PATH}...")
df = pd.read_csv(DATA_PATH)
df.fillna("", inplace=True)
df["text"] = df["name"] + " " + df["description"]

X = df["text"]
y = df["label"]

# Recreate the exact split from training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
)

print(f"Loading model from {MODEL_PATH}...")
pipeline = joblib.load(MODEL_PATH)

print("Evaluating Fake Consultancy Model on test data...")
y_pred = pipeline.predict(X_test)

# Calculate individual metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"Accuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall:    {recall * 100:.2f}%")
print(f"F1-score:  {f1 * 100:.2f}%")

# Generate a detailed report for each class (Fake vs. Real)
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Real Consultancy', 'Fake Consultancy']))
# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# Plot Confusion Matrix
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Real Consultancy','Fake Consultancy'],
            yticklabels=['Real Consultancy','Fake Consultancy'])

plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix - Fake Consultancy Detection")
plt.show()
# ROC Curve
y_prob = pipeline.predict_proba(X_test)[:,1]

fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, color='blue', label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0,1],[0,1], color='read', linestyle='--')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Fake Consultancy Detection")
plt.legend(loc="lower right")

plt.show()

# Learning Curve
train_sizes, train_scores, test_scores = learning_curve(
    pipeline, X, y,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 5)
)

train_mean = np.mean(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)

plt.figure(figsize=(7,5))
plt.plot(train_sizes, train_mean, label="Training Score", marker='o')
plt.plot(train_sizes, test_mean, label="Cross-validation Score", marker='o')

plt.xlabel("Training Examples")
plt.ylabel("Accuracy")
plt.title("Learning Curve")
plt.legend()
plt.grid()

plt.show()