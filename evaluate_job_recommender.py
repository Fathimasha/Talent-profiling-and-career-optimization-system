import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity as _cosine_sim

# ---- Load Data ----
print("Loading jobs dataset...")
jobs = pd.read_csv("data/jobs.csv")

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

jobs["full_text"] = (
    jobs["Responsibilities"].fillna("")
    + " "
    + jobs["Keywords"].fillna("")
    + " "
    + jobs["Skills"].fillna("")
)
jobs["clean_description"] = jobs["full_text"].apply(preprocess_text)
jobs_df_clean = jobs.dropna(subset=["job_title", "ExperienceLevel"]).drop_duplicates(
    subset=["job_title", "ExperienceLevel"]
).copy()
jobs_df_clean.reset_index(drop=True, inplace=True)

# ---- Embeddings (SBERT) ----
print("Generating Job Embeddings with SBERT...")
model = SentenceTransformer("all-MiniLM-L6-v2")
job_embeddings = model.encode(
    jobs_df_clean["clean_description"].tolist(),
    convert_to_numpy=True,
    show_progress_bar=True,
)

# ---- Helper Functions ----
def clean_split_skills(text):
    parts = re.split(r"[;,/]", str(text).lower())
    return [p.strip() for p in parts if p.strip()]

def compute_skill_score(job_skills, resume_skills):
    job_skill_list = clean_split_skills(job_skills)
    resume_skill_list = clean_split_skills(resume_skills)
    if len(job_skill_list) == 0:
        return 0.0
    common = set(resume_skill_list).intersection(set(job_skill_list))
    return len(common) / len(job_skill_list)

# Metrics
def precision_at_k(recommended, relevant, k=3):
    recommended_k = recommended[:k]
    hits = len(set(recommended_k) & set(relevant))
    return hits / k

def recall_at_k(recommended, relevant, k=3):
    recommended_k = recommended[:k]
    hits = len(set(recommended_k) & set(relevant))
    if len(relevant) == 0:
        return 0
    return hits / len(relevant)

def f1_score_at_k(p, r):
    if p + r == 0:
        return 0
    return 2 * (p * r) / (p + r)

def ndcg_at_k(recommended, relevant, k=3):
    dcg = 0
    for i, job in enumerate(recommended[:k]):
        if job in relevant:
            dcg += 1 / np.log2(i + 2)
    ideal_dcg = sum([1 / np.log2(i + 2) for i in range(min(len(relevant), k))])
    if ideal_dcg == 0:
        return 0
    return dcg / ideal_dcg

# ---- Recommendation System Evaluation ----
print("Evaluating Recommendation System (Precision@3, Recall@3, F1@3, NDCG@3)...")
k = 3

precisions = []
recalls = []
f1_scores = []
ndcgs = []

# Filter jobs_df_clean to only jobs with multiple occurrences of the same title
title_counts = jobs_df_clean['job_title'].value_counts()
valid_titles = title_counts[title_counts > 1].index

test_pool = jobs_df_clean[jobs_df_clean['job_title'].isin(valid_titles)]

# Sample Resumes User Input
np.random.seed(42)
test_size = min(100, len(test_pool))
test_indices = np.random.choice(test_pool.index, size=test_size, replace=False)

for idx in test_indices:
    resume_row = jobs_df_clean.loc[idx]
    resume_title = resume_row["job_title"]
    resume_emb = job_embeddings[idx].reshape(1, -1)
    resume_skills = str(resume_row["Skills"])
    
    # 1. ACTUAL RELEVANT JOBS
    relevant_indices = jobs_df_clean[
        (jobs_df_clean["job_title"] == resume_title) & (jobs_df_clean.index != idx)
    ].index.tolist()
    
    # 2. SYSTEM RECOMMENDS TOP-3
    scores = np.zeros(len(jobs_df_clean))
    semantic_sims = _cosine_sim(resume_emb, job_embeddings)[0]
    
    for i in range(len(jobs_df_clean)):
        if i == idx:
            scores[i] = -1
            continue
        skill_score = compute_skill_score(jobs_df_clean.at[i, "Skills"], resume_skills)
        scores[i] = (semantic_sims[i] * 0.7) + (skill_score * 0.3)
        
    top_k_indices = scores.argsort()[-k:][::-1].tolist()
    
    # 3. COMPARE & CALCULATE METRICS
    p = precision_at_k(top_k_indices, relevant_indices, k)
    r = recall_at_k(top_k_indices, relevant_indices, k)
    f1 = f1_score_at_k(p, r)
    ndcg = ndcg_at_k(top_k_indices, relevant_indices, k)
    
    precisions.append(p)
    recalls.append(r)
    f1_scores.append(f1)
    ndcgs.append(ndcg)

# 4. AVERAGE METRICS
print("\n--- Recommendation Engine Evaluation Results ---")
print(f"Sample Size Evaluated: {len(precisions)} simulated resumes")
print(f"Average Precision@{k}: {np.mean(precisions)*100:.2f}%")
print(f"Average Recall@{k}: {np.mean(recalls)*100:.2f}%")
print(f"Average F1@{k}: {np.mean(f1_scores)*100:.2f}%")
print(f"Average NDCG@{k}: {np.mean(ndcgs)*100:.2f}%")