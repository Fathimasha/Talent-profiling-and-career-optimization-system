# src/services/consultancy_service.py
from src.database.consultancy_db import lookup_consultancy_in_dataset
from src.ml.consultancy_classifier import predict_consultancy_ml

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

        return {
            "error": "Consultancy not found in database. Please provide description for ML analysis."
        }

    # Case 2: Name + description -> ML model
    return predict_consultancy_ml(name, description, asks_fee)
