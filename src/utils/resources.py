# src/utils/resources.py
from src.utils.text_processing import normalize_skill_name

SKILL_RESOURCES = {
    "python": [
        {
            "title": "Python full course for beginners (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=python+full+course+for+beginners",
            "provider": "YouTube",
        },
        {
            "title": "Official Python tutorial",
            "url": "https://docs.python.org/3/tutorial/",
            "provider": "python.org",
        },
    ],
    "java": [
        {
            "title": "Java programming for beginners (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=java+programming+full+course+for+beginners",
            "provider": "YouTube",
        }
    ],
    "c": [
        {
            "title": "C language beginner course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=c+programming+full+course",
            "provider": "YouTube",
        }
    ],
    "c++": [
        {
            "title": "C++ programming full course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=c%2B%2B+programming+full+course",
            "provider": "YouTube",
        }
    ],
    "c#": [
        {
            "title": "C# and .NET for beginners (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=c%23+dotnet+full+course+for+beginners",
            "provider": "YouTube",
        }
    ],
    ".net": [
        {
            "title": ".NET / ASP.NET beginner tutorials (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=asp.net+core+full+course",
            "provider": "YouTube",
        }
    ],
    "javascript": [
        {
            "title": "JavaScript full course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=javascript+full+course+for+beginners",
            "provider": "YouTube",
        }
    ],
    "html": [
        {
            "title": "HTML & CSS crash course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=html+css+full+course",
            "provider": "YouTube",
        }
    ],
    "css": [
        {
            "title": "Modern CSS layouts & flexbox (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=css+flexbox+grid+tutorial",
            "provider": "YouTube",
        }
    ],
    "react": [
        {
            "title": "React JS full course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=react+js+full+course+for+beginners",
            "provider": "YouTube",
        },
        {
            "title": "React official docs",
            "url": "https://react.dev/learn",
            "provider": "react.dev",
        },
    ],
    "nodejs": [
        {
            "title": "Node.js API & backend course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=node+js+api+rest+full+course",
            "provider": "YouTube",
        }
    ],
    "springboot": [
        {
            "title": "Spring Boot REST API course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=spring+boot+rest+api+full+course",
            "provider": "YouTube",
        }
    ],
    "flask": [
        {
            "title": "Flask web app tutorial (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=flask+web+app+tutorial",
            "provider": "YouTube",
        }
    ],
    "django": [
        {
            "title": "Django full stack course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=django+full+stack+course",
            "provider": "YouTube",
        }
    ],
    "sql": [
        {
            "title": "SQL for data analysis (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=sql+for+beginners+full+course",
            "provider": "YouTube",
        }
    ],
    "mysql": [
        {
            "title": "MySQL database tutorial (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=mysql+database+tutorial+for+beginners",
            "provider": "YouTube",
        }
    ],
    "postgresql": [
        {
            "title": "PostgreSQL tutorial (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=postgresql+tutorial+for+beginners",
            "provider": "YouTube",
        }
    ],
    "mongodb": [
        {
            "title": "MongoDB for beginners (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=mongodb+for+beginners",
            "provider": "YouTube",
        }
    ],
    "machine learning": [
        {
            "title": "Machine learning full course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=machine+learning+full+course",
            "provider": "YouTube",
        }
    ],
    "deep learning": [
        {
            "title": "Deep learning tutorial (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=deep+learning+neural+networks+full+course",
            "provider": "YouTube",
        }
    ],
    "nlp": [
        {
            "title": "NLP with Python course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=nlp+with+python+tutorial",
            "provider": "YouTube",
        }
    ],
    "data science": [
        {
            "title": "Data science roadmap & course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=data+science+full+course",
            "provider": "YouTube",
        }
    ],
    "pandas": [
        {
            "title": "Pandas tutorial (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=pandas+python+tutorial",
            "provider": "YouTube",
        }
    ],
    "numpy": [
        {
            "title": "NumPy tutorial (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=numpy+python+tutorial",
            "provider": "YouTube",
        }
    ],
    "scikit learn": [
        {
            "title": "scikit-learn ML course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=scikit+learn+tutorial",
            "provider": "YouTube",
        }
    ],
    "tensorflow": [
        {
            "title": "TensorFlow 2 tutorial (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=tensorflow+2+tutorial",
            "provider": "YouTube",
        }
    ],
    "keras": [
        {
            "title": "Keras deep learning tutorial (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=keras+deep+learning+tutorial",
            "provider": "YouTube",
        }
    ],
    "pytorch": [
        {
            "title": "PyTorch for deep learning (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=pytorch+for+deep+learning+full+course",
            "provider": "YouTube",
        }
    ],
    "android": [
        {
            "title": "Android app development with Kotlin (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=android+app+development+with+kotlin+full+course",
            "provider": "YouTube",
        }
    ],
    "kotlin": [
        {
            "title": "Kotlin for Android beginners (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=kotlin+android+tutorial",
            "provider": "YouTube",
        }
    ],
    "firebase": [
        {
            "title": "Firebase for web/mobile apps (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=firebase+tutorial",
            "provider": "YouTube",
        }
    ],
    "aws": [
        {
            "title": "AWS cloud practitioner / developer course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=aws+cloud+practitioner+full+course",
            "provider": "YouTube",
        }
    ],
    "azure": [
        {
            "title": "Microsoft Azure fundamentals (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=azure+fundamentals+full+course",
            "provider": "YouTube",
        }
    ],
    "gcp": [
        {
            "title": "Google Cloud Platform (GCP) basics (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=google+cloud+platform+for+beginners",
            "provider": "YouTube",
        }
    ],
    "docker": [
        {
            "title": "Docker containers & images (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=docker+for+beginners+full+course",
            "provider": "YouTube",
        }
    ],
    "kubernetes": [
        {
            "title": "Kubernetes for developers (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=kubernetes+for+beginners+full+course",
            "provider": "YouTube",
        }
    ],
    "git": [
        {
            "title": "Git & GitHub crash course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=git+and+github+crash+course",
            "provider": "YouTube",
        }
    ],
    "github": [
        {
            "title": "GitHub basics for developers (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=github+tutorial+for+beginners",
            "provider": "YouTube",
        }
    ],
    "linux": [
        {
            "title": "Linux command line basics (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=linux+command+line+for+beginners",
            "provider": "YouTube",
        }
    ],
    "excel": [
        {
            "title": "Excel for data analysis (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=excel+for+data+analysis+full+course",
            "provider": "YouTube",
        }
    ],
    "power bi": [
        {
            "title": "Power BI beginner to pro (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=power+bi+full+course",
            "provider": "YouTube",
        }
    ],
    "tableau": [
        {
            "title": "Tableau data visualization course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=tableau+data+visualization+tutorial",
            "provider": "YouTube",
        }
    ],
}

def get_resources_for_skill(skill: str):
    key = normalize_skill_name(skill)
    return SKILL_RESOURCES.get(key, [])

ROLE_RESOURCES = {
    ".net_developer": [
        {
            "title": "🧭 .NET Developer Roadmap (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=.net+developer+roadmap",
            "provider": "YouTube",
        },
        {
            "title": "C# and ASP.NET Core full course (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=c%23+asp.net+core+full+course",
            "provider": "YouTube",
        },
    ],
    "data_scientist": [
        {
            "title": "🧭 Data Scientist Roadmap (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=data+scientist+roadmap",
            "provider": "YouTube",
        },
        {
            "title": "End-to-end data science project tutorials",
            "url": "https://www.youtube.com/results?search_query=data+science+project+end+to+end",
            "provider": "YouTube",
        },
    ],
    "ml_engineer": [
        {
            "title": "🧭 Machine Learning Engineer Roadmap (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=machine+learning+engineer+roadmap",
            "provider": "YouTube",
        },
        {
            "title": "Deploying ML models to production",
            "url": "https://www.youtube.com/results?search_query=deploy+machine+learning+models+to+production",
            "provider": "YouTube",
        },
    ],
    "full_stack": [
        {
            "title": "🧭 Full-Stack Developer Roadmap (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=full+stack+developer+roadmap",
            "provider": "YouTube",
        },
        {
            "title": "MERN / full-stack web app tutorial",
            "url": "https://www.youtube.com/results?search_query=full+stack+web+app+project+mern",
            "provider": "YouTube",
        },
    ],
    "frontend": [
        {
            "title": "🧭 Frontend Developer Roadmap (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=frontend+developer+roadmap",
            "provider": "YouTube",
        },
        {
            "title": "React + modern frontend course",
            "url": "https://www.youtube.com/results?search_query=react+js+frontend+developer+course",
            "provider": "YouTube",
        },
    ],
    "backend": [
        {
            "title": "🧭 Backend Developer Roadmap (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=backend+developer+roadmap",
            "provider": "YouTube",
        },
        {
            "title": "REST API design and best practices",
            "url": "https://www.youtube.com/results?search_query=rest+api+design+best+practices",
            "provider": "YouTube",
        },
    ],
    "android": [
        {
            "title": "🧭 Android Developer Roadmap (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=android+developer+roadmap",
            "provider": "YouTube",
        },
        {
            "title": "Android app with Kotlin full course",
            "url": "https://www.youtube.com/results?search_query=android+app+development+with+kotlin+full+course",
            "provider": "YouTube",
        },
    ],
    "data_analyst": [
        {
            "title": "🧭 Data Analyst Roadmap (YouTube search)",
            "url": "https://www.youtube.com/results?search_query=data+analyst+roadmap",
            "provider": "YouTube",
        },
        {
            "title": "Excel, SQL, and Power BI for data analysis",
            "url": "https://www.youtube.com/results?search_query=excel+sql+power+bi+data+analysis+course",
            "provider": "YouTube",
        },
    ],
}

def get_role_key(job_title: str) -> str:
    t = str(job_title).lower()
    if ".net" in t or "dotnet" in t or "c#" in t:
        return ".net_developer"
    if "data scientist" in t or "data science" in t:
        return "data_scientist"
    if "machine learning engineer" in t or "ml engineer" in t:
        return "ml_engineer"
    if "full stack" in t or "full-stack" in t:
        return "full_stack"
    if "frontend" in t or "front-end" in t or "ui developer" in t:
        return "frontend"
    if "backend" in t or "back-end" in t:
        return "backend"
    if "android" in t or "mobile developer" in t:
        return "android"
    if "data analyst" in t or ("business analyst" in t and "data" in t):
        return "data_analyst"
    return ""

def get_role_resources(job_title: str):
    key = get_role_key(job_title)
    if not key:
        return []
    return ROLE_RESOURCES.get(key, [])
