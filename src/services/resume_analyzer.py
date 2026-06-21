# src/services/resume_analyzer.py
import re
from src.utils.text_processing import clean_split_skills, normalize_skill_name

# ATS Compatibility Constants
_ATS_STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'shall', 'can', 'need', 'must',
    'we', 'you', 'he', 'she', 'it', 'they', 'i', 'me', 'him', 'her',
    'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their',
    'this', 'that', 'these', 'those', 'what', 'which', 'who', 'whom',
    'not', 'no', 'nor', 'as', 'if', 'then', 'than', 'too', 'very',
    'just', 'about', 'above', 'after', 'again', 'all', 'also', 'any',
    'because', 'before', 'between', 'both', 'each', 'few', 'more',
    'most', 'other', 'over', 'same', 'so', 'some', 'such', 'through',
    'under', 'until', 'up', 'while', 'into', 'out', 'during', 'how',
    'when', 'where', 'why', 'able', 'etc', 'including', 'well',
    'looking', 'role', 'position', 'job', 'company', 'team', 'work',
    'working', 'within', 'across', 'using', 'used', 'use', 'new',
    'good', 'great', 'strong', 'excellent', 'preferred', 'required',
    'requirements', 'responsibilities', 'qualifications', 'experience',
    'years', 'year', 'minimum', 'plus', 'knowledge', 'skills',
    'ability', 'understanding', 'environment', 'opportunity',
}

_ATS_MULTI_WORD_TERMS = [
    'machine learning', 'deep learning', 'data science',
    'natural language processing', 'computer vision',
    'project management', 'version control', 'ci cd',
    'continuous integration', 'continuous deployment',
    'data analysis', 'data engineering', 'web development',
    'mobile development', 'cloud computing', 'big data',
    'artificial intelligence', 'software development',
    'agile methodology', 'scrum master', 'product management',
    'user experience', 'user interface', 'full stack',
    'front end', 'back end', 'rest api', 'unit testing',
    'test driven', 'object oriented', 'problem solving',
    'software engineering', 'system design', 'microservices',
    'distributed systems', 'data structures', 'design patterns',
]

_ATS_POWER_VERBS = [
    'achieved', 'implemented', 'developed', 'managed', 'led',
    'optimized', 'designed', 'built', 'created', 'improved',
    'analyzed', 'collaborated', 'delivered', 'reduced', 'increased',
    'automated', 'architected', 'streamlined', 'mentored', 'launched',
]

_RESUME_SECTIONS = {
    'Contact Information': ['email', 'phone', 'linkedin', 'github', 'address', 'contact', 'mobile'],
    'Professional Summary': ['summary', 'objective', 'profile', 'about me', 'career objective', 'professional summary'],
    'Skills': ['skills', 'technical skills', 'core competencies', 'technologies', 'proficiencies'],
    'Work Experience': ['experience', 'work experience', 'employment', 'professional experience', 'work history', 'internship'],
    'Education': ['education', 'academic', 'degree', 'university', 'college', 'bachelor', 'master', 'b.tech', 'b.e', 'm.tech'],
    'Certifications': ['certification', 'certifications', 'certified', 'certificate', 'licenses', 'credentials'],
}

def generate_resume_suggestions(resume_text, resume_skills, top_k):
    """Generate structured, rule-based resume improvement suggestions."""
    suggestions = {
        "missing_skills": [],
        "content": [],
        "formatting": [],
    }
    text_lower = str(resume_text).lower()

    # A) Missing Technical Skills
    all_missing = set()
    for _, row in top_k.iterrows():
        for skill in row.get("missing_skills", []):
            if skill:
                all_missing.add(skill)

    if all_missing:
        pretty_skills = ", ".join(sorted({s.title() for s in all_missing}))
        suggestions["missing_skills"].append(
            f"Highlight or start learning these in-demand skills that appear in your top matching roles: {pretty_skills}."
        )
    else:
        suggestions["missing_skills"].append(
            "Your resume already covers most of the key technical skills required for the recommended roles. Consider keeping them clearly grouped in a dedicated Skills section."
        )

    # B) Resume Content Improvements
    word_count = len(re.findall(r"\w+", str(resume_text)))
    if word_count < 300:
        suggestions["content"].append(
            "Your resume appears relatively short. Consider adding more detail about projects, responsibilities, and achievements (aim for at least 300–500 words)."
        )

    if "project" not in text_lower:
        suggestions["content"].append(
            "Add a dedicated 'Projects' section showcasing 2–4 key projects with technologies used, your role, and impact."
        )

    action_verbs = [
        "achieved",
        "developed",
        "built",
        "implemented",
        "designed",
        "created",
        "improved",
        "led",
        "optimized",
        "automated",
    ]
    if not any(verb in text_lower for verb in action_verbs):
        suggestions["content"].append(
            "Use strong action verbs (e.g., 'developed', 'built', 'implemented', 'optimized') at the start of bullet points to make your experience more impactful."
        )

    if not re.search(r"\d|%", str(resume_text)):
        suggestions["content"].append(
            "Include measurable results where possible (e.g., 'improved accuracy by 15%', 'reduced processing time by 30%', 'handled 50+ customer queries per day')."
        )

    # C) Formatting Suggestions (always helpful)
    suggestions["formatting"].extend(
        [
            "Use clear section headings such as 'Summary', 'Skills', 'Experience', 'Projects', and 'Education' to make the resume easy to scan.",
            "Prefer concise bullet points instead of long paragraphs so recruiters and ATS can quickly parse your experience.",
            "Group technical skills by category (e.g., Programming Languages, Frameworks, Databases, Cloud, Tools) for better readability.",
            "Keep the layout ATS-friendly: avoid text inside tables or images, use simple fonts, and ensure consistent alignment and spacing.",
        ]
    )

    return suggestions

def analyze_ats_compatibility(raw_resume_text, resume_skills, job_description):
    """Full ATS compatibility analysis of resume against a job description."""
    results = {}
    jd_lower = job_description.lower()
    resume_lower = raw_resume_text.lower()

    # ── Extract keywords from job description ──
    found_multi = set()
    for term in _ATS_MULTI_WORD_TERMS:
        if term in jd_lower:
            found_multi.add(term)

    jd_words = re.findall(r'\b[a-z][a-z0-9#+.]+\b', jd_lower)
    word_freq = {}
    for w in jd_words:
        if w not in _ATS_STOPWORDS and len(w) > 2:
            word_freq[w] = word_freq.get(w, 0) + 1

    sorted_kw = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    top_single = {w for w, _ in sorted_kw[:40]}
    all_jd_keywords = top_single | found_multi

    matched_keywords = {kw for kw in all_jd_keywords if kw in resume_lower}
    missing_keywords = all_jd_keywords - matched_keywords

    recommended = {v for v in _ATS_POWER_VERBS if v in jd_lower and v not in resume_lower}

    results['matched_keywords'] = sorted(matched_keywords)
    results['missing_keywords'] = sorted(missing_keywords)
    results['recommended_keywords'] = sorted(recommended)

    # ── Section structure check ──
    section_scores = {}
    section_suggestions = {}

    for section, keywords in _RESUME_SECTIONS.items():
        found = any(kw in resume_lower for kw in keywords)

        if section == 'Contact Information':
            has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', raw_resume_text))
            has_phone = bool(re.search(r'[\+]?[\d\s\-().]{7,}', raw_resume_text))
            if has_email and has_phone:
                score, tip = 100, "Contact information is complete."
            elif has_email or has_phone:
                score, tip = 60, "Add both email and phone number."
            else:
                score, tip = 20, "Add clear contact information (email, phone, LinkedIn)."

        elif section == 'Professional Summary':
            if found:
                score, tip = 85, "Summary detected. Tailor it to the target role with relevant keywords."
            else:
                score, tip = 30, "Add a Professional Summary (3-4 lines) highlighting key qualifications."

        elif section == 'Skills':
            if len(resume_skills) > 10:
                score, tip = 95, "Strong skills section with excellent coverage."
            elif len(resume_skills) > 5:
                score, tip = 75, "Good skills listed. Add more relevant skills from the job description."
            elif len(resume_skills) > 0:
                score, tip = 55, "Skills section is thin. Add more relevant technical skills."
            else:
                score, tip = 20, "Add a dedicated Skills section."

        elif section == 'Work Experience':
            if found:
                has_metrics = bool(re.search(r'\d+\s*%|\d+\+|reduced|increased|improved|saved', resume_lower))
                has_verbs = any(v in resume_lower for v in _ATS_POWER_VERBS[:10])
                if has_metrics and has_verbs:
                    score, tip = 95, "Excellent — quantified achievements with action verbs."
                elif has_verbs:
                    score, tip = 75, "Good action verbs. Add quantified achievements (numbers, %)."
                else:
                    score, tip = 55, "Use action verbs and include measurable results."
            else:
                score, tip = 25, "Add a Work Experience section with titles, companies, dates, and achievements."

        elif section == 'Education':
            if found:
                score, tip = 90, "Education section present."
            else:
                score, tip = 30, "Add an Education section with degree, institution, and graduation year."

        else:  # Certifications
            if found:
                score, tip = 90, "Certifications detected — great addition!"
            else:
                score, tip = 50, "Consider adding relevant certifications."

        section_scores[section] = score
        section_suggestions[section] = tip

    results['section_scores'] = section_scores
    results['section_suggestions'] = section_suggestions

    # ── Formatting assessment ──
    formatting_checks = {}

    word_count = len(re.findall(r'\w+', raw_resume_text))
    if 300 <= word_count <= 1000:
        formatting_checks['Resume Length'] = (True, f"Good length ({word_count} words)")
    elif word_count < 300:
        formatting_checks['Resume Length'] = (False, f"Too short ({word_count} words). Aim for 400-800 words.")
    else:
        formatting_checks['Resume Length'] = (True, f"Detailed resume ({word_count} words). Consider condensing to 2 pages.")

    formatting_checks['ATS-Safe Format'] = (True, "PDF text is extractable — ATS compatible.")

    has_bullets = bool(re.search(r'[•\-\*►▪■]', raw_resume_text))
    formatting_checks['Bullet Points'] = (
        has_bullets,
        "Uses bullet points for readability." if has_bullets else "Add bullet points for experience entries."
    )

    has_dates = bool(re.search(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{4})', resume_lower))
    formatting_checks['Date Formatting'] = (
        has_dates,
        "Dates detected in resume." if has_dates else "Add dates to experience and education entries."
    )

    heading_count = sum(
        1 for keywords in _RESUME_SECTIONS.values()
        if any(kw in resume_lower for kw in keywords)
    )
    formatting_checks['Section Headings'] = (
        heading_count >= 4,
        f"{heading_count}/6 standard sections detected." if heading_count >= 4
        else f"Only {heading_count}/6 standard sections found. Add clear headings."
    )

    results['formatting_checks'] = formatting_checks

    # ── Overall ATS score ──
    keyword_score = (len(matched_keywords) / max(len(all_jd_keywords), 1)) * 30

    resume_skill_lower = {s.lower() for s in resume_skills}
    jd_skill_tokens = set(re.findall(r'\b[a-z][a-z0-9#+.]+\b', jd_lower))
    skill_overlap = len(resume_skill_lower & jd_skill_tokens) / max(len(resume_skill_lower | jd_skill_tokens), 1)
    skill_match_score = skill_overlap * 25

    section_avg = sum(section_scores.values()) / max(len(section_scores), 1)
    section_score = (section_avg / 100) * 20

    fmt_passed = sum(1 for ok, _ in formatting_checks.values() if ok)
    fmt_score = (fmt_passed / max(len(formatting_checks), 1)) * 15

    contact_score = (section_scores.get('Contact Information', 50) / 100) * 10

    total = keyword_score + skill_match_score + section_score + fmt_score + contact_score
    results['overall_score'] = min(round(total), 100)
    results['score_breakdown'] = {
        'Keyword Match (30)': round(keyword_score, 1),
        'Skills Alignment (25)': round(skill_match_score, 1),
        'Section Structure (20)': round(section_score, 1),
        'Formatting (15)': round(fmt_score, 1),
        'Contact Info (10)': round(contact_score, 1),
    }

    # ── Optimization tips with rewrite examples ──
    top_kw = list(matched_keywords)[:3] + list(missing_keywords)[:2]
    kw_display = ', '.join(k.title() for k in top_kw[:5]) or 'relevant technologies'
    skill_display = ', '.join(s.title() for s in list(resume_skills)[:3]) or 'key technologies'
    all_relevant = sorted(set(list(matched_keywords)[:4] + list(resume_skills)[:4]))

    results['optimization_tips'] = [
        {
            'section': 'Professional Summary',
            'before': "Experienced software professional looking for new opportunities.",
            'after': f"Results-driven professional with expertise in {kw_display}, seeking to leverage proven skills in building scalable solutions that drive measurable business impact.",
        },
        {
            'section': 'Experience Bullet Points',
            'before': "Worked on developing web applications using various technologies.",
            'after': f"Developed and deployed 5+ production applications using {skill_display}, resulting in 40% improvement in system performance and user engagement.",
        },
        {
            'section': 'Skills Section',
            'before': "Skills: Python, Java, SQL",
            'after': "Technical Skills: " + ' | '.join(s.title() for s in all_relevant[:8])
                     + "\nTools & Platforms: Git, Docker, AWS, CI/CD Pipeline",
        },
    ]

    return results
