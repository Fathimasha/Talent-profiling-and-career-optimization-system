# src/utils/text_processing.py
import re

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def compute_text_overlap(text_a, text_b):
    """Fallback: simple word-overlap score when SBERT unavailable."""
    words_a = set(re.findall(r"\b[a-z0-9]+\b", text_a.lower()))
    words_b = set(re.findall(r"\b[a-z0-9]+\b", text_b.lower()))
    if not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_b)

def clean_split_skills(text):
    parts = re.split(r"[;,/]", str(text).lower())
    return [p.strip() for p in parts if p.strip()]

def normalize_skill_name(skill: str) -> str:
    s = str(skill).strip().lower()
    # Remove common suffixes
    s = re.sub(r"\s+(basics?|fundamentals?)$", "", s)
    # Normalizations / aliases
    if s in {"js"}:
        return "javascript"
    if s in {"node.js", "node js"}:
        return "nodejs"
    if s in {"sql server", "t-sql"}:
        return "sql"
    if s in {"powerbi", "power-bi"}:
        return "power bi"
    if s in {"ml"}:
        return "machine learning"
    if s in {"dl"}:
        return "deep learning"
    if s in {"c sharp", "c#"}:
        return "c#"
    if s in {".net", "dotnet", ".net core", ".net framework"}:
        return ".net"
    return s
