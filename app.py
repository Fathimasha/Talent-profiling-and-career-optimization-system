import streamlit as st
from src.database.loader import load_data
from src.services.job_recommender import prepare_job_data
from src.ui.sidebar import render_sidebar
from src.ui.career_guidance import render_career_guidance_page
from src.ui.consultancy_checker import render_consultancy_checker_page

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Page Config ──
# set_page_config MUST be the first Streamlit command in the script
st.set_page_config(
    page_title="AI Career Compass Pro",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load global CSS styling
load_css("style.css")

# ── Load Datasets ──
jobs_df, courses_df = load_data()

# ── Prepare Job Recommendation Data & Embeddings ──
prepare_job_data(jobs_df)

# ── Render Navigation Sidebar ──
selected_page = render_sidebar()

# ── Page Routing ──
if selected_page == "Career Guidance":
    render_career_guidance_page()
elif selected_page == "Fake Jobs & Consultancies":
    render_consultancy_checker_page()