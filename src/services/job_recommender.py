# src/services/job_recommender.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from src.config import USE_SEMANTIC, sbert_model, cosine_similarity
from src.utils.text_processing import (
    preprocess_text,
    compute_text_overlap,
    clean_split_skills,
    normalize_skill_name,
)

# Globally cached/prepared job data and embeddings
jobs_df_clean = None
job_embeddings = None

def prepare_job_data(jobs_df):
    global jobs_df_clean, job_embeddings
    
    jobs_df["full_text"] = (
        jobs_df["Responsibilities"].fillna("")
        + " "
        + jobs_df["Keywords"].fillna("")
        + " "
        + jobs_df["Skills"].fillna("")
    )
    jobs_df["clean_description"] = jobs_df["full_text"].apply(preprocess_text)
    jobs_df_clean = jobs_df.dropna(subset=["job_title", "ExperienceLevel"]).drop_duplicates(
        subset=["job_title", "ExperienceLevel"]
    ).copy()
    
    if USE_SEMANTIC and sbert_model is not None:
        job_embeddings = sbert_model.encode(
            jobs_df_clean["clean_description"].tolist(),
            convert_to_numpy=True,
            show_progress_bar=False,
        )
    return jobs_df_clean

def get_job_recommendations(resume_text, resume_skills):
    global jobs_df_clean, job_embeddings
    
    if jobs_df_clean is None:
        raise ValueError("Job data has not been prepared. Call prepare_job_data first.")
        
    df_copy = jobs_df_clean.copy()
    
    # Compute semantic scores
    if USE_SEMANTIC and sbert_model is not None and job_embeddings is not None:
        resume_embedding = sbert_model.encode([resume_text], convert_to_numpy=True)
        semantic_scores = cosine_similarity(resume_embedding, job_embeddings)[0]
        df_copy["semantic_score"] = np.clip(semantic_scores, 0, 1)
    else:
        df_copy["semantic_score"] = df_copy["clean_description"].apply(
            lambda jd: compute_text_overlap(resume_text, jd)
        )
        
    # Compute skill scores
    def compute_skill_score(job_skills):
        job_skill_list = clean_split_skills(job_skills)
        if len(job_skill_list) == 0:
            return 0
        norm_resume = {normalize_skill_name(sk) for sk in resume_skills}
        norm_job = {normalize_skill_name(sk) for sk in job_skill_list}
        common = norm_resume.intersection(norm_job)
        return len(common) / len(job_skill_list)
        
    df_copy["skill_score"] = df_copy["Skills"].apply(compute_skill_score)
    
    # Classification / Relevance training
    rel_sem, rel_skill = 0.35, 0.2
    if not USE_SEMANTIC:
        rel_sem, rel_skill = 0.1, 0.15
        
    df_copy["relevant"] = (
        (df_copy["semantic_score"] > rel_sem)
        | (df_copy["skill_score"] > rel_skill)
    ).astype(int)
    
    X = df_copy[["semantic_score", "skill_score"]]
    y = df_copy["relevant"]
    
    rf = RandomForestClassifier(n_estimators=120, random_state=42)
    
    if len(y.unique()) > 1:
        rf.fit(X, y)
        df_copy["rf_score"] = rf.predict_proba(X)[:, 1]
    else:
        df_copy["rf_score"] = df_copy["semantic_score"]
        
    # Top 3 jobs
    top_k = df_copy.sort_values(by="rf_score", ascending=False).head(3).copy()
    
    # Compute skill gaps
    def skill_gap(job_skills):
        job_skill_list = clean_split_skills(job_skills)
        norm_resume = {normalize_skill_name(sk) for sk in resume_skills}
        missing = [sk for sk in job_skill_list if normalize_skill_name(sk) not in norm_resume]
        return sorted(list(set(missing)))
        
    top_k["missing_skills"] = top_k["Skills"].apply(skill_gap)
    
    return top_k
