# src/database/loader.py
import streamlit as st
import pandas as pd
from src.config import JOBS_CSV_PATH, COURSES_CSV_PATH

@st.cache_data
def load_data():
    jobs = pd.read_csv(JOBS_CSV_PATH)
    courses = pd.read_csv(COURSES_CSV_PATH)
    return jobs, courses
