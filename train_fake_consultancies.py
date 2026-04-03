# ==========================================================
# Research-Grade Fake Consultancy Detection Training Script
# ==========================================================

import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.utils.class_weight import compute_class_weight

# ---------------- CONFIG ----------------
DATA_PATH = "data/consultancies_dataset.csv"
MODEL_PATH = "models/fake_consultancy_research.pkl"

RANDOM_STATE = 42
TEST_SIZE = 0.2

# ---------------- LOAD DATA ----------------
print(f"Loading dataset from {DATA_PATH} ...")
df = pd.read_csv(DATA_PATH)

# Required columns
required_cols = ["name", "description", "asks_fee", "label"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

df.fillna("", inplace=True)

# Combine name + description
df["text"] = df["name"] + " " + df["description"]

X = df["text"]
y = df["label"]

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=TEST_SIZE,
    stratify=y,
    random_state=RANDOM_STATE
)

print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

# ---------------- CLASS WEIGHTS ----------------
classes = np.unique(y_train)
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train
)

class_weight_dict = dict(zip(classes, class_weights))

# ---------------- PIPELINE ----------------
model = LogisticRegression(
    max_iter=2000,
    class_weight=class_weight_dict,
    random_state=RANDOM_STATE
)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.9,
        sublinear_tf=True
    )),
    ("classifier", model)
])

# ---------------- CROSS VALIDATION ----------------
print("Performing 5-fold cross-validation...")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1")

print(f"CV F1 Scores: {cv_scores}")
print(f"Mean CV F1: {cv_scores.mean():.4f}")

# ---------------- TRAIN ----------------
print("Training final model...")
pipeline.fit(X_train, y_train)

# ---------------- EVALUATE ----------------
print("Evaluating on hold-out set...")
y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"F1-score: {f1 * 100:.2f}%")
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred))

# ---------------- SAVE ----------------
os.makedirs("models", exist_ok=True)
joblib.dump(pipeline, MODEL_PATH)

print(f"\nSaved model to {MODEL_PATH}")