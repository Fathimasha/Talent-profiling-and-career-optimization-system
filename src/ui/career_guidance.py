# src/ui/career_guidance.py
import re
import pdfplumber
import numpy as np
import streamlit as st
import plotly.graph_objects as go

from src.config import USE_SEMANTIC
from src.ml.skill_extractor import extract_skills_from_pdf
from src.utils.text_processing import preprocess_text, clean_split_skills, normalize_skill_name
from src.utils.resources import get_resources_for_skill
from src.services.job_recommender import get_job_recommendations
from src.services.resume_analyzer import generate_resume_suggestions, analyze_ats_compatibility

def render_career_guidance_page():
    # ── Hero Section ──
    st.markdown(
        """
    <div class="hero-container">
        <div class="hero-title">AI Career Compass Pro</div>
        <div class="hero-subtitle">
            Upload your resume and let AI find your perfect career match.
            Get personalized job recommendations, skill gap analysis, and curated courses.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Upload Section ──
    col_pad_l, col_upload, col_pad_r = st.columns([1, 2, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF)",
            type=["pdf"],
            label_visibility="collapsed",
        )
        st.markdown(
            '<p style="text-align:center; color:#64748b; font-size:0.82rem; margin-top:0.5rem;">'
            "Drag & drop or click to upload your PDF resume</p>",
            unsafe_allow_html=True,
        )

    if uploaded_file is None:
        st.markdown("---")
        feat_cols = st.columns(3)
        features = [
            (
                "🔍",
                "Smart Matching",
                "Semantic AI + skill-based matching for accurate job recommendations",
            ),
            (
                "📊",
                "Gap Analysis",
                "Identify missing skills between your profile and dream roles",
            ),
            (
                "🎓",
                "Course Paths",
                "Get curated Coursera courses to bridge your skill gaps",
            ),
        ]
        for col, (icon, title, desc) in zip(feat_cols, features):
            with col:
                st.markdown(
                    f"""
                <div class="stats-card" style="min-height: 160px; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="font-size: 1rem; font-weight: 700; color: #e2e8f0; margin-bottom: 0.5rem;">{title}</div>
                    <div style="font-size: 0.82rem; color: #94a3b8; line-height: 1.5;">{desc}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        st.stop()

    # ── Process Resume ──
    with st.spinner("Analyzing your resume..."):
        with pdfplumber.open(uploaded_file) as pdf:
            resume_text = ""
            for page in pdf.pages:
                resume_text += page.extract_text() or ""

        resume_text_raw = resume_text
        resume_text = preprocess_text(resume_text)

        if len(resume_text.strip()) == 0:
            st.error(
                "Could not extract readable text from the PDF. Please try a different file."
            )
            st.stop()

        # Reset file so skill extractor can read from the beginning
        uploaded_file.seek(0)
        resume_skills = extract_skills_from_pdf(uploaded_file)

        # Get job recommendations using recommender service
        top_k = get_job_recommendations(resume_text, resume_skills)

    # ── Success Banner ──
    st.markdown(
        """
    <div class="success-banner">
        <span style="font-size: 1.2rem;">&#10003;</span>
        Resume analyzed successfully &mdash; here are your personalized results
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)

    # ── Quick Stats ──
    total_missing = sum(len(row["missing_skills"]) for _, row in top_k.iterrows())
    avg_score = top_k["rf_score"].mean()

    stat_cols = st.columns(4)
    stats = [
        (str(len(resume_skills)), "Skills Detected"),
        (f"{avg_score:.0%}", "Avg Match Score"),
        (str(total_missing), "Skill Gaps Found"),
        ("3", "Jobs Matched"),
    ]
    for col, (num, label) in zip(stat_cols, stats):
        with col:
            st.markdown(
                f"""
            <div class="stats-card">
                <div class="stats-number">{num}</div>
                <div class="stats-label">{label}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # ── Extracted Skills ──
    st.markdown(
        """
    <div class="section-header">
        <div class="section-icon">🧠</div>
        <div class="section-title">Your Skills Profile</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if len(resume_skills) == 0:
        st.warning("No skills were detected. Try uploading a more detailed resume.")
    else:
        skills_html = "".join(
            f'<span class="skill-badge">{skill.title()}</span>'
            for skill in sorted(resume_skills)
        )
        st.markdown(
            f'<div style="padding: 0.5rem 0;">{skills_html}</div>',
            unsafe_allow_html=True,
        )

    # ── Job Recommendations ──
    st.markdown(
        """
    <div class="section-header">
        <div class="section-icon">💼</div>
        <div class="section-title">Top Job Recommendations</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    job_cols = st.columns(3)
    for idx, (col, (_, row)) in enumerate(zip(job_cols, top_k.iterrows())):
        score = row["rf_score"]
        score_pct = min(score * 100, 100)

        if score >= 0.7:
            bar_color = "linear-gradient(90deg, #10b981, #06b6d4)"
        elif score >= 0.4:
            bar_color = "linear-gradient(90deg, #6366f1, #818cf8)"
        else:
            bar_color = "linear-gradient(90deg, #f59e0b, #fbbf24)"

        exp = row.get("ExperienceLevel", "N/A")
        yrs = row.get("YearsOfExperience", "")
        exp_display = f"{exp}" + (f" ({yrs} yrs)" if yrs else "")

        matched_count = int(
            round(row["skill_score"] * len(clean_split_skills(row["Skills"])))
        )
        total_skills = len(clean_split_skills(row["Skills"]))

        with col:
            st.markdown(
                f"""
            <div class="job-card">
                <div class="job-rank">#{idx + 1}</div>
                <div class="job-title">{row['job_title']}</div>
                <div class="job-meta">
                    <span class="meta-tag">&#128188; {exp_display}</span>
                    <span class="meta-tag">&#9989; {matched_count}/{total_skills} skills</span>
                </div>
                <div class="score-bar-container">
                    <div class="score-label">
                        <span>Match Score</span>
                        <span style="font-weight:600; color:#a5b4fc;">{score:.1%}</span>
                    </div>
                    <div class="score-bar-bg">
                        <div class="score-bar-fill" style="width:{score_pct}%; background:{bar_color};"></div>
                    </div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # ── Match Score Radar Chart ──
    st.markdown(
        """
    <div class="section-header">
        <div class="section-icon">📈</div>
        <div class="section-title">Match Breakdown</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    chart_cols = st.columns([2, 1])

    with chart_cols[0]:
        fig = go.Figure()

        for _, row in top_k.iterrows():
            coverage_val = 1 - (len(row["missing_skills"]) / max(len(clean_split_skills(row["Skills"])), 1))
            fig.add_trace(
                go.Scatterpolar(
                    r=[
                        row["semantic_score"],
                        row["skill_score"],
                        row["rf_score"],
                        coverage_val,
                        row["semantic_score"],
                    ],
                    theta=[
                        "Semantic Match",
                        "Skill Match",
                        "Overall Score",
                        "Coverage",
                        "Semantic Match",
                    ],
                    fill="toself",
                    name=row["job_title"],
                    opacity=0.6,
                )
            )

        fig.update_layout(
            polar=dict(
                bgcolor="rgba(30, 41, 59, 0.5)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    gridcolor="rgba(99, 102, 241, 0.15)",
                    linecolor="rgba(99, 102, 241, 0.2)",
                ),
                angularaxis=dict(
                    gridcolor="rgba(99, 102, 241, 0.15)",
                    linecolor="rgba(99, 102, 241, 0.2)",
                ),
            ),
            showlegend=True,
            legend=dict(font=dict(color="#94a3b8", size=11)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            margin=dict(l=40, r=40, t=30, b=30),
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_cols[1]:
        st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
        for idx, (_, row) in enumerate(top_k.iterrows()):
            st.markdown(
                f"""
            <div style="background: #1e293b; border-radius: 10px; padding: 0.75rem; margin-bottom: 0.5rem; border: 1px solid rgba(99,102,241,0.1);">
                <div style="font-size: 0.82rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.5rem;">#{idx+1} {row['job_title']}</div>
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8; margin-bottom: 2px;">
                    <span>Semantic</span><span style="color:#a5b4fc; font-weight:600;">{row['semantic_score']:.3f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8; margin-bottom: 2px;">
                    <span>Skill</span><span style="color:#a5b4fc; font-weight:600;">{row['skill_score']:.3f}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #94a3b8;">
                    <span>Final</span><span style="color:#06b6d4; font-weight:600;">{row['rf_score']:.3f}</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Skill Gap Analysis ──
    st.markdown(
        """
    <div class="section-header">
        <div class="section-icon">📉</div>
        <div class="section-title">Skill Gap Analysis</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    for _, row in top_k.iterrows():
        st.markdown(
            f'<div class="gap-job-header">{row["job_title"]}</div>',
            unsafe_allow_html=True,
        )

        if len(row["missing_skills"]) == 0:
            st.markdown(
                '<div class="no-gaps-badge">&#10024; No major skill gaps — great match!</div>',
                unsafe_allow_html=True,
            )
        else:
            job_skill_list = clean_split_skills(row["Skills"])
            norm_resume = {normalize_skill_name(sk) for sk in resume_skills}
            matched_html = ""
            missing_html = ""
            for s in sorted(set(job_skill_list)):
                if normalize_skill_name(s) in norm_resume:
                    matched_html += (
                        f'<span class="skill-badge matched">{s.title()}</span>'
                    )
                elif s in row["missing_skills"]:
                    missing_html += (
                        f'<span class="skill-badge missing">{s.title()}</span>'
                    )

            combined = matched_html + missing_html
            st.markdown(
                f'<div style="padding: 0.25rem 0 0.75rem 0;">{combined}</div>',
                unsafe_allow_html=True,
            )

            pct = len(row["missing_skills"]) / max(len(job_skill_list), 1)
            st.markdown(
                f"""
            <div style="font-size: 0.78rem; color: #94a3b8; margin-bottom: 0.75rem;">
                <span style="color: #6ee7b7;">&#9679;</span> You have &nbsp;|&nbsp;
                <span style="color: #fca5a5;">&#9679;</span> Missing ({len(row['missing_skills'])} of {len(job_skill_list)} &mdash; {pct:.0%} gap)
            </div>
            """,
                unsafe_allow_html=True,
            )

    # ── Course / Learning Recommendations ──
    st.markdown(
        """
    <div class="section-header">
        <div class="section-icon">🎓</div>
        <div class="section-title">Recommended Learning Resources</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="color:#94a3b8; font-size:0.88rem; margin-bottom:1rem;">'
        "Curated YouTube searches and official documentation to help you learn the skills required for your target roles.</p>",
        unsafe_allow_html=True,
    )

    tab_labels = [f"📋 {row['job_title']}" for _, row in top_k.iterrows()]
    tab_labels.append("📝 Resume Improvement")
    tabs = st.tabs(tab_labels)

    job_tabs = tabs[:-1]
    improve_tab = tabs[-1]

    for tab, (_, row) in zip(job_tabs, top_k.iterrows()):
        with tab:
            if len(row["missing_skills"]) == 0:
                st.markdown(
                    '<div class="no-gaps-badge" style="margin: 1rem 0;">&#127881; No skill gaps to fill — you\'re all set!</div>',
                    unsafe_allow_html=True,
                )
                continue

            shown = set()
            resource_count = 0
            for skill in row["missing_skills"]:
                resources = get_resources_for_skill(skill)
                for res in resources:
                    title = res.get("title", f"Learn {skill.title()}")
                    url = res.get("url", "#")
                    provider = res.get("provider", "Resource")
                    key = (title, url)
                    if key in shown:
                        continue
                    shown.add(key)
                    resource_count += 1

                    st.markdown(
                        f"""
                    <a href="{url}" target="_blank" class="course-link" style="text-decoration: none;">
                        <div class="course-card">
                            <div class="course-icon">&#128218;</div>
                            <div class="course-info">
                                <div class="course-skill">Learn: {skill.title()}</div>
                                <div class="course-title">{title}</div>
                                <div class="course-provider">
                                    {provider}
                                </div>
                            </div>
                        </div>
                    </a>
                    """,
                        unsafe_allow_html=True,
                    )

            if resource_count == 0:
                st.markdown(
                    '<p style="color: #64748b; font-style: italic; padding: 1rem 0;">No mapped resources found for these skills yet. You can manually search on YouTube or official docs.</p>',
                    unsafe_allow_html=True,
                )

    with improve_tab:
        suggestions = generate_resume_suggestions(resume_text, resume_skills, top_k)

        st.markdown(
            '<p style="color:#94a3b8; font-size:0.88rem; margin:0.5rem 0 1rem 0;">'
            "Rule-based tips to make your resume stronger, clearer, and better aligned with your target roles."
            "</p>",
            unsafe_allow_html=True,
        )

        # A) Missing Technical Skills
        if suggestions["missing_skills"]:
            bullets = "".join(f"<li>{s}</li>" for s in suggestions["missing_skills"])
            st.markdown(
                f"""
                <div class="card-improve">
                    <h4>🔹 Missing Technical Skills</h4>
                    <ul>
                        {bullets}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="card-improve">
                    <h4>🔹 Missing Technical Skills</h4>
                    <p>No major missing technical skills detected for your top recommended jobs.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # B) Resume Content Improvements
        if suggestions["content"]:
            bullets = "".join(f"<li>{s}</li>" for s in suggestions["content"])
            st.markdown(
                f"""
                <div class="card-improve">
                    <h4>🔹 Resume Content Improvements</h4>
                    <ul>
                        {bullets}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="card-improve">
                    <h4>🔹 Resume Content Improvements</h4>
                    <p>Your content already looks substantial and action-oriented. Great work!</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # C) Formatting Suggestions
        if suggestions["formatting"]:
            bullets = "".join(f"<li>{s}</li>" for s in suggestions["formatting"])
            st.markdown(
                f"""
                <div class="card-improve">
                    <h4>🔹 Formatting Suggestions</h4>
                    <ul>
                        {bullets}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="card-improve">
                    <h4>🔹 Formatting Suggestions</h4>
                    <p>Formatting suggestions are not available at the moment.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── ATS Resume Analyzer Section ──
    st.markdown(
        """
    <div class="section-header">
        <div class="section-icon">📊</div>
        <div class="section-title">ATS Resume Analyzer</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="color:#94a3b8; font-size:0.88rem; margin-bottom:1rem;">'
        "Paste a target job description below and click <strong>Analyze ATS Compatibility</strong> "
        "to see how well your resume matches, with keyword analysis, section scores, and optimization tips."
        "</p>",
        unsafe_allow_html=True,
    )

    ats_job_desc = st.text_area(
        "Paste the target job description",
        placeholder="Paste the full job description here to analyze ATS compatibility...",
        height=180,
        key="ats_jd_input",
    )

    ats_btn_col1, ats_btn_col2, ats_btn_col3 = st.columns([1, 1, 1])
    with ats_btn_col2:
        ats_analyze = st.button("🔍 Analyze ATS Compatibility", use_container_width=True, type="primary")

    if ats_analyze:
        if not ats_job_desc.strip():
            st.error("Please paste a non-empty job description to analyze.")
        else:
            with st.spinner("Running ATS analysis..."):
                ats_results = analyze_ats_compatibility(resume_text_raw, resume_skills, ats_job_desc)

            score = ats_results['overall_score']
            if score >= 75:
                score_color = "#10b981"
                score_label = "Excellent"
            elif score >= 50:
                score_color = "#f59e0b"
                score_label = "Good — Needs Improvement"
            else:
                score_color = "#ef4444"
                score_label = "Low — Significant Changes Needed"

            # ── Score display + breakdown ──
            score_col, breakdown_col = st.columns([1, 1.5])

            with score_col:
                st.markdown(
                    f"""
                <div class="ats-score-container">
                    <div class="ats-score-ring" style="background: conic-gradient({score_color} {score * 3.6}deg, #1e293b {score * 3.6}deg);">
                        <div class="ats-score-inner">
                            <div class="ats-score-value" style="color: {score_color};">{score}%</div>
                            <div class="ats-score-label">ATS Score</div>
                        </div>
                    </div>
                    <div class="ats-score-verdict" style="color: {score_color};">{score_label}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with breakdown_col:
                st.markdown('<div class="ats-breakdown-title">Score Breakdown</div>', unsafe_allow_html=True)
                for category, pts in ats_results['score_breakdown'].items():
                    max_pts = int(re.search(r'\((\d+)\)', category).group(1))
                    pct = (pts / max_pts) * 100 if max_pts else 0
                    cat_label = re.sub(r'\s*\(\d+\)', '', category)
                    if pct >= 70:
                        bar_clr = "#10b981"
                    elif pct >= 40:
                        bar_clr = "#f59e0b"
                    else:
                        bar_clr = "#ef4444"
                    st.markdown(
                        f"""
                    <div class="ats-bar-row">
                        <div class="ats-bar-label">{cat_label}</div>
                        <div class="ats-bar-track">
                            <div class="ats-bar-fill" style="width:{pct}%; background:{bar_clr};"></div>
                        </div>
                        <div class="ats-bar-value">{pts}/{max_pts}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

            # ── Keyword Analysis ──
            st.markdown(
                """
            <div class="ats-sub-header">🔑 Keyword Analysis</div>
            """,
                unsafe_allow_html=True,
            )

            kw_col1, kw_col2, kw_col3 = st.columns(3)

            with kw_col1:
                matched = ats_results['matched_keywords']
                badges = ''.join(f'<span class="ats-kw-badge matched">{k}</span>' for k in matched) if matched else '<span style="color:#64748b;">None</span>'
                st.markdown(
                    f"""
                <div class="ats-kw-card">
                    <div class="ats-kw-header matched">✅ Matched Keywords ({len(matched)})</div>
                    <div class="ats-kw-body">{badges}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with kw_col2:
                missing = ats_results['missing_keywords']
                badges = ''.join(f'<span class="ats-kw-badge missing">{k}</span>' for k in missing) if missing else '<span style="color:#64748b;">None</span>'
                st.markdown(
                    f"""
                <div class="ats-kw-card">
                    <div class="ats-kw-header missing">❌ Missing Keywords ({len(missing)})</div>
                    <div class="ats-kw-body">{badges}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with kw_col3:
                recommended = ats_results['recommended_keywords']
                badges = ''.join(f'<span class="ats-kw-badge recommended">{k}</span>' for k in recommended) if recommended else '<span style="color:#64748b;">None</span>'
                st.markdown(
                    f"""
                <div class="ats-kw-card">
                    <div class="ats-kw-header recommended">⚠️ Recommended to Add ({len(recommended)})</div>
                    <div class="ats-kw-body">{badges}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # ── Section-wise Score Breakdown ──
            st.markdown(
                '<div class="ats-sub-header">📋 Section-wise Score Breakdown</div>',
                unsafe_allow_html=True,
            )

            sec_cols = st.columns(3)
            for idx, (section, sec_score) in enumerate(ats_results['section_scores'].items()):
                suggestion = ats_results['section_suggestions'][section]
                if sec_score >= 80:
                    sec_clr = "#10b981"
                    sec_icon = "✅"
                elif sec_score >= 50:
                    sec_clr = "#f59e0b"
                    sec_icon = "⚠️"
                else:
                    sec_clr = "#ef4444"
                    sec_icon = "❌"

                with sec_cols[idx % 3]:
                    st.markdown(
                        f"""
                    <div class="ats-section-card">
                        <div class="ats-section-top">
                            <span>{sec_icon} {section}</span>
                            <span class="ats-section-score" style="color:{sec_clr};">{sec_score}/100</span>
                        </div>
                        <div class="ats-section-bar-bg">
                            <div class="ats-section-bar-fill" style="width:{sec_score}%; background:{sec_clr};"></div>
                        </div>
                        <div class="ats-section-tip">{suggestion}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

            # ── Formatting & Structure Evaluation ──
            st.markdown(
                '<div class="ats-sub-header">🔍 Formatting & Structure Evaluation</div>',
                unsafe_allow_html=True,
            )

            for check_name, (passed, detail) in ats_results['formatting_checks'].items():
                icon = "✅" if passed else "❌"
                clr = "#6ee7b7" if passed else "#fca5a5"
                st.markdown(
                    f"""
                <div class="ats-check-row">
                    <span style="font-size:1.1rem;">{icon}</span>
                    <div>
                        <span class="ats-check-name">{check_name}</span>
                        <span class="ats-check-detail" style="color:{clr};">{detail}</span>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # ── Resume Optimization Tips (Before / After) ──
            st.markdown(
                '<div class="ats-sub-header">✏️ Resume Optimization Tips — Rewrite Examples</div>',
                unsafe_allow_html=True,
            )

            for tip in ats_results['optimization_tips']:
                st.markdown(
                    f"""
                <div class="ats-tip-card">
                    <div class="ats-tip-section">{tip['section']}</div>
                    <div class="ats-tip-row">
                        <div class="ats-tip-label before">Before</div>
                        <div class="ats-tip-text before">{tip['before']}</div>
                    </div>
                    <div class="ats-tip-row">
                        <div class="ats-tip-label after">After</div>
                        <div class="ats-tip-text after">{tip['after']}</div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # ── Actionable Improvement Suggestions ──
            st.markdown(
                '<div class="ats-sub-header">🎯 Actionable Improvement Suggestions</div>',
                unsafe_allow_html=True,
            )

            action_items = []
            if ats_results['missing_keywords']:
                top_missing = ', '.join(k.title() for k in ats_results['missing_keywords'][:8])
                action_items.append(f"Add these missing keywords to relevant sections of your resume: <strong>{top_missing}</strong>")

            if ats_results['recommended_keywords']:
                rec_str = ', '.join(k.title() for k in ats_results['recommended_keywords'][:5])
                action_items.append(f"Use these power verbs in your experience bullet points: <strong>{rec_str}</strong>")

            for section, sec_score in ats_results['section_scores'].items():
                if sec_score < 60:
                    action_items.append(f"Improve your <strong>{section}</strong> section — {ats_results['section_suggestions'][section]}")

            for check_name, (passed, detail) in ats_results['formatting_checks'].items():
                if not passed:
                    action_items.append(f"Fix <strong>{check_name}</strong>: {detail}")

            action_items.append("Quantify achievements with numbers and percentages wherever possible.")
            action_items.append("Mirror the exact job title and key phrases from the job description in your resume.")

            bullets = ''.join(f'<li>{item}</li>' for item in action_items)
            st.markdown(
                f"""
            <div class="ats-action-card">
                <ul>{bullets}</ul>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # ── Footer ──
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <div style="font-size: 0.82rem; color: #475569;">
            Built with Streamlit &amp; Sentence-BERT &nbsp;&#x2022;&nbsp; AI Career Compass Pro
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
