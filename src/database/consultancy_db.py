# src/database/consultancy_db.py
import pandas as pd
from src.config import CONSULTANCIES_CSV_PATH

# Load consultancy dataset globally
try:
    consultancies_df = pd.read_csv(CONSULTANCIES_CSV_PATH)
except Exception as e:
    print(f"Error loading consultancy dataset: {e}")
    consultancies_df = pd.DataFrame(columns=["name", "description", "asks_fee", "label"])

def lookup_consultancy_in_dataset(name: str):
    """
    Look up a consultancy by (partial) name in the labelled dataset.
    Returns a result dict if found, otherwise None.
    """
    if not name or consultancies_df.empty:
        return None

    name_lower = name.strip().lower()

    # Case-insensitive, partial match to make the lookup user-friendly
    matches = consultancies_df[
        consultancies_df["name"].str.lower().str.contains(name_lower, na=False)
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
