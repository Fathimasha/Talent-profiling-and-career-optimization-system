# src/config.py
import os

# Data and Model File Paths
JOBS_CSV_PATH = "data/jobs.csv"
COURSES_CSV_PATH = "data/webautomation_coursera.csv"
CONSULTANCIES_CSV_PATH = "data/consultancies_dataset.csv"
CONSULTANCY_MODEL_PATH = "models/fake_consultancy_research.pkl"

# Sentence-BERT configurations
USE_SEMANTIC = False
sbert_model = None
cosine_similarity = None

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity as _cosine_sim

    cosine_similarity = _cosine_sim
    sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
    USE_SEMANTIC = True
except ImportError:
    pass
