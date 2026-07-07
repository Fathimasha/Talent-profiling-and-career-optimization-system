# 🚀 AI Career Compass Pro

An intelligent AI-powered career guidance and resume analysis platform that leverages **Deep Learning**, **Semantic Similarity**, and **Skill Ontology** to evaluate resumes and recommend suitable career paths.

The system analyzes a candidate's resume, understands the semantic meaning of skills using transformer models, compares them against predefined career profiles, and provides accurate career recommendations with similarity scores.

---

# ✨ Features

- 📄 AI Resume Analysis
- 🧠 Semantic Skill Matching
- 🔍 Hybrid Similarity Engine
- 🎯 Career Recommendation
- 📊 Similarity Score Visualization
- 🗂️ Skill Ontology-Based Matching
- ⚡ Interactive Streamlit Dashboard
- 🤖 Transformer-Based Deep Learning Model

---

# 🧠 AI Technologies Used

### 🔹 Sentence-BERT (SBERT)

Uses the **all-MiniLM-L6-v2** transformer model to generate high-quality sentence embeddings and understand the semantic meaning of resumes beyond simple keyword matching.

### 🔹 Hybrid Similarity Engine

The recommendation engine combines two approaches:

- **Semantic Cosine Similarity**
- **Ontology-Based Lexical Matching**

This hybrid approach improves recommendation accuracy by considering both contextual meaning and exact skill relationships.

### 🔹 Skill Ontology

A structured hierarchy that maps technical skills to domains and career roles, enabling more intelligent and explainable recommendations.

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| AI Framework | Sentence Transformers (SBERT) |
| Machine Learning | Deep Learning |
| Similarity Metrics | Cosine Similarity + Ontology Matching |
| Frontend | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib / Plotly *(if used)* |

---

# 📂 Project Structure

```text
AI-Career-Compass-Pro/
│
├── app.py
├── requirements.txt
├── ontology/
├── datasets/
├── models/
├── utils/
├── assets/
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/AI-Career-Compass-Pro.git
```

```bash
cd AI-Career-Compass-Pro
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run the Application

```bash
streamlit run app.py
```

---

# 📌 First-Time Setup

During the first execution, the application automatically downloads the pretrained **Sentence-BERT** model:

```
all-MiniLM-L6-v2
```

This may take a few minutes depending on your internet connection.

After downloading, subsequent launches will be significantly faster.

---

# 🔄 Workflow

```text
Resume Upload
        │
        ▼
Resume Preprocessing
        │
        ▼
Sentence-BERT Embedding Generation
        │
        ▼
Hybrid Similarity Calculation
        │
        ├── Semantic Cosine Similarity
        └── Ontology-Based Skill Matching
        │
        ▼
Career Recommendation
        │
        ▼
Similarity Scores & Results
```

---

# 🎯 Core Components

### 📄 Resume Processing
- Extracts and preprocesses resume text
- Identifies technical skills and keywords

### 🤖 Semantic Embedding
- Converts resumes into dense vector representations using SBERT

### 🔍 Hybrid Similarity
- Measures semantic similarity
- Performs ontology-aware lexical matching
- Combines both scores for improved recommendation accuracy

### 💼 Career Recommendation
- Matches resumes with career profiles
- Returns ranked recommendations
- Displays confidence/similarity scores

---

# 🚀 Future Enhancements

- 📁 PDF & DOCX Resume Upload
- 🤖 LLM-Based Resume Feedback
- 🎓 Course Recommendations
- 📈 Skill Gap Analysis
- 🌐 Job Portal Integration
- 🧾 Resume Score Prediction
- 🧠 Personalized Learning Roadmaps
- ☁️ Cloud Deployment

---

# 📚 Technologies & Concepts

- Deep Learning
- Sentence Transformers (SBERT)
- Transformer Models
- Natural Language Processing (NLP)
- Semantic Text Similarity
- Cosine Similarity
- Skill Ontology
- Information Retrieval
- Streamlit
- Python

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is intended for **educational, research, and learning purposes**.

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!
