# src/ui/sidebar.py
import streamlit as st
from src.config import USE_SEMANTIC

def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
        <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🧭</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #a5b4fc; letter-spacing: -0.01em;">
                Career Compass
            </div>
            <div style="font-size: 0.78rem; color: #64748b; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 2px;">
                AI-Powered Guidance
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown(
            """
        <div style="padding: 0 0.5rem;">
            <p style="font-size: 0.85rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.75rem;">How it works</p>
            <div style="display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="min-width: 28px; height: 28px; background: linear-gradient(135deg, #6366f1, #4f46e5); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: white;">1</div>
                <div style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.5;">Upload your resume in PDF format</div>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="min-width: 28px; height: 28px; background: linear-gradient(135deg, #6366f1, #4f46e5); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: white;">2</div>
                <div style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.5;">AI extracts your skills &amp; matches jobs</div>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="min-width: 28px; height: 28px; background: linear-gradient(135deg, #6366f1, #4f46e5); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: white;">3</div>
                <div style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.5;">Get personalized job &amp; course recommendations</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        if not USE_SEMANTIC:
            st.warning(
                "**Skill-only mode** — Install `sentence-transformers` for full AI semantic matching.",
                icon="⚠️",
            )
        st.markdown(
            """
        <div style="padding: 0 0.5rem;">
            <p style="font-size: 0.85rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.5rem;">Powered by</p>
            <div style="font-size: 0.8rem; color: #94a3b8; line-height: 1.8;">
                &#x2022; Sentence-BERT (NLP)<br>
                &#x2022; Random Forest Classifier<br>
                &#x2022; Cosine Similarity Matching<br>
                &#x2022; 1,000+ Job Listings<br>
                &#x2022; 280+ Coursera Courses
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        selected_page = st.radio(
            "Navigation",
            ["Career Guidance", "Fake Jobs & Consultancies"],
            index=0,
        )
    return selected_page
