import os
import numpy as np
import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.class_weight import compute_class_weight

DATA_PATH = "data/consultancies_dataset.csv"
MODEL_PATH = "models/fake_consultancy_rf.pkl"

def main():
    print(f"Loading data from {DATA_PATH} ...")
    df = pd.read_csv(DATA_PATH)

    # Ensure required columns exist
    required = ["name", "description", "asks_fee", "label"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column in dataset: {col}")

    df["name"] = df["name"].fillna("")
    df["description"] = df["description"].fillna("")
    df["asks_fee"] = df["asks_fee"].fillna(0).astype(float)
    y = df["label"].astype(int).values

    print("Loading Sentence-BERT model...")
    sbert = SentenceTransformer("all-MiniLM-L6-v2")

    print("Encoding name and description with SBERT...")
    name_emb = sbert.encode(
        df["name"].tolist(),
        convert_to_numpy=True,
        show_progress_bar=True,
    )
    desc_emb = sbert.encode(
        df["description"].tolist(),
        convert_to_numpy=True,
        show_progress_bar=True,
    )

    fee_feature = df["asks_fee"].values.reshape(-1, 1)

    # Feature vector: [name_emb | desc_emb | asks_fee]
    X = np.concatenate([name_emb, desc_emb, fee_feature], axis=1)

    # Class weights for imbalance
    classes = np.unique(y)
    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=y,
    )
    class_weight_dict = dict(zip(classes, class_weights))

    print("Training RandomForest classifier...")
    clf = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight=class_weight_dict,
        n_jobs=-1,
    )
    clf.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"Saved consultancy RF model to {MODEL_PATH}")

if __name__ == "__main__":
    main()