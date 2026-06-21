# src/ml/consultancy_classifier.py
import os
import joblib
from src.config import CONSULTANCY_MODEL_PATH

# Try to load trained model globally
model = None
if os.path.exists(CONSULTANCY_MODEL_PATH):
    try:
        model = joblib.load(CONSULTANCY_MODEL_PATH)
    except Exception as e:
        print(f"Error loading ML model from {CONSULTANCY_MODEL_PATH}: {e}")

def get_ml_model():
    return model

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

    # The model/pipeline expects an iterable of strings
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
