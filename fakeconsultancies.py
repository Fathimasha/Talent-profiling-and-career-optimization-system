"""
Consultancy Legitimacy Checker
------------------------------

Inference helpers for:
- Database lookup on the labelled consultancy dataset
- ML model using Logistic Regression
"""

import os
import joblib
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration / resources
# ---------------------------------------------------------------------------

DATA_PATH = "data/consultancies_dataset.csv"
MODEL_PATH = "models/fake_consultancy_research.pkl"  # Logistic Regression

# Load labelled consultancy dataset (also used for database lookup)
consultancies = pd.read_csv(DATA_PATH)

# Try to load trained Logistic Regression model
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
    except Exception:
        model = None
else:
    model = None


# ---------------------------------------------------------------------------
# Core helper functions
# ---------------------------------------------------------------------------

def lookup_consultancy_in_dataset(name: str):
    """
    Look up a consultancy by (partial) name in the labelled dataset.

    Returns a result dict if found, otherwise None.
    """
    if not name:
        return None

    name_lower = name.strip().lower()

    # Case-insensitive, partial match to make the lookup user-friendly
    matches = consultancies[
        consultancies["name"].str.lower().str.contains(name_lower, na=False)
    ]

    if matches.empty:
        return None

    row = matches.iloc[0]
    is_fake = int(row["label"]) == 1

    return {
        "label": "Fake Consultancy" if is_fake else "Real Consultancy",
        "confidence": 100.0,
        "fake_probability": 100.0 if is_fake else 0.0,
        "real_probability": 0.0 if is_fake else 100.0,
        "source": "Database Lookup",
    }


def predict_consultancy_ml(name: str, description: str, asks_fee: bool):
    """
    Run the Logistic Regression classifier purely on the text and return
    prediction details including confidence and per-class probabilities.
    """
    if model is None:
        return {
            "error": (
                "Consultancy ML model file not found or could not be loaded. "
                "Train it and save as 'models/fake_consultancy_research.pkl' to enable ML analysis."
            )
        }
        
    text = name + " " + description

    # The new pipeline expects an iterable of strings
    pred = model.predict([text])[0]
    proba = model.predict_proba([text])[0]

    fake_prob = float(proba[1])
    real_prob = float(proba[0])
    is_fake = int(pred) == 1

    label = "Fake Consultancy" if is_fake else "Real Consultancy"
    confidence = fake_prob if is_fake else real_prob

    return {
        "label": label,
        "confidence": round(confidence * 100.0, 2),
        "fake_probability": round(fake_prob * 100.0, 2),
        "real_probability": round(real_prob * 100.0, 2),
        "source": "ML Model",
    }


def predict_consultancy(name: str, description: str = "", asks_fee: bool = False):
    """
    Main prediction entrypoint.

    Logic:
    - If description is empty:
        * Perform database lookup using the consultancy dataset.
        * If found -> return stored label, 100% confidence, source=Database Lookup.
        * If not found -> return an error message instructing the user to
          provide a description for ML analysis.
    - If description is provided:
        * Pass the text to the Logistic Regression classifier.
    """
    name = (name or "").strip()
    description = (description or "").strip()

    if not name:
        raise ValueError("Consultancy name is required for prediction.")

    # Case 1: Name only -> database lookup
    if not description:
        db_result = lookup_consultancy_in_dataset(name)
        if db_result is not None:
            return db_result

        # Modify to be friendly if they only entered a name, still predict but with 100% confidence error
        return {
            "error": "Consultancy not found in database. Please provide description for ML analysis."
        }

    # Case 2: Name + description -> ML model
    return predict_consultancy_ml(name, description, asks_fee)
