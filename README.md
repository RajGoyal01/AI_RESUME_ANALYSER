# 🤖 AI Resume Analyser

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.1-black?style=for-the-badge&logo=flask&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-spaCy%20%7C%20NLTK-green?style=for-the-badge)
![ML](https://img.shields.io/badge/ML-scikit--learn-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**An AI-powered resume evaluation tool that compares resumes against job descriptions, scores them intelligently, and provides actionable improvement suggestions.**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Project Structure](#-project-structure) • [How It Works](#-how-it-works)

</div>

---

## 📌 Overview

In today's competitive job market, thousands of resumes are submitted for a single opening, and recruiters rely heavily on **Applicant Tracking Systems (ATS)** to filter candidates. Many qualified applicants get rejected not because of lack of skill — but due to poorly structured resumes or missing keywords.

The **AI Resume Analyser** bridges this gap by:

- Automatically scanning resumes (PDF/DOC format)
- Extracting key information using NLP
- Comparing resumes against job descriptions
- Providing an intelligent match score and targeted improvement suggestions

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Multi-format Support** | Accepts PDF and DOC/DOCX resume files |
| 🔍 **Smart Text Extraction** | Handles multi-column layouts, tables, and graphic-heavy resumes |
| 🧠 **NLP Analysis** | Extracts skills, education, and experience using spaCy & NLTK |
| 📊 **Match Scoring** | Cosine Similarity-based algorithm for resume-to-job-description alignment |
| ⚖️ **Weighted Scoring** | Prioritizes skills for technical roles, experience for senior roles |
| 💡 **Gap Detection** | Identifies missing critical keywords and suggests improvements |
| 🔄 **Synonym Matching** | Custom synonym dictionary prevents keyword-miss errors |
| 🖼️ **Visual Dashboard** | Progress bars and visual data summaries for easy interpretation |
| ⚡ **Fast Processing** | Processes graphic-heavy resumes in under 3 seconds |
| 🌐 **Web Interface** | Clean, interactive frontend built with HTML/CSS/JS |

---

## 🛠️ Tech Stack

### Backend
- **Python** — Core language
- **Flask** — Web framework and REST API
- **spaCy / NLTK** — Natural Language Processing
- **scikit-learn** — Cosine Similarity scoring
- **pdfplumber / PyPDF2** — PDF text extraction
- **python-docx** — DOCX file handling
- **pytesseract / EasyOCR / Pillow** — OCR for image-based or scanned PDFs

### Frontend
- **HTML5 / CSS3 / JavaScript** — Interactive user interface

---

## 📁 Project Structure

```
AI_RESUME_ANALYSER/
│
├── backend/                  # Flask application & NLP logic
│   ├── app.py                # Main Flask server
│   ├── parser.py             # Resume text extraction module
│   ├── analyser.py           # NLP processing & scoring engine
│   └── ...
│
├── frontend/                 # Web interface
│   ├── index.html            # Main UI page
│   ├── style.css             # Styling
│   └── script.js             # Frontend logic
│
├── requirements.txt          # Python dependencies
├── start_server.bat          # One-click startup script (Windows)
└── .gitignore
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- pip
- Tesseract OCR installed on your system ([Download here](https://github.com/UB-Mannheim/tesseract/wiki))

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/RajGoyal01/AI_RESUME_ANALYSER.git
cd AI_RESUME_ANALYSER
```

**2. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**3. Download spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

**4. Download NLTK data**
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

**5. Start the server**

On Windows (quick start):
```
start_server.bat
```

Or manually:
```bash
cd backend
python app.py
```

**6. Open in browser**
```
http://localhost:5000
```

---

## 🚀 Usage

1. **Upload your resume** — supports PDF or DOCX format
2. **Paste the job description** — of the role you're applying for
3. **Click Analyse** — the system processes your resume in seconds
4. **View your results:**
   - ✅ Match Score (%)
   - 🟡 Missing Skills / Keywords
   - 📈 Strengths & Weaknesses breakdown
   - 💬 Actionable improvement suggestions

---

## 🔬 How It Works

```
User Uploads Resume (PDF/DOC)
        ↓
Text Extraction (pdfplumber / PyPDF2 / EasyOCR)
        ↓
Data Cleaning & Preprocessing
        ↓
NLP Processing (spaCy / NLTK)
  → Tokenization
  → Stop-word Removal
  → Named Entity Recognition
  → Keyword Extraction (Skills, Education, Experience)
        ↓
Job Description Comparison
  → Cosine Similarity Scoring
  → Synonym Matching
  → Weighted Parameter Scoring
        ↓
Result Generation
  → Match Score
  → Missing Keywords
  → Suggestions
        ↓
Display on UI (Visual Dashboard)
```

---

## 📦 Dependencies

```
flask==3.1.1
flask-cors==5.0.1
PyPDF2==3.0.1
pdfplumber==0.11.6
python-docx==1.1.2
spacy==3.8.4
scikit-learn==1.6.1
nltk==3.9.1
Werkzeug==3.1.3
pytesseract==0.3.13
Pillow==11.1.0
easyocr==1.7.2
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🗺️ Future Roadmap

- [ ] Integration with LinkedIn profiles
- [ ] Job portal API connections (Naukri, Indeed, etc.)
- [ ] AI-based interview preparation suggestions
- [ ] Support for multiple job description comparisons simultaneously
- [ ] User accounts and resume history tracking
- [ ] Deployment on cloud (AWS / Render / Railway)

---

## 📊 Project Development Timeline

| Week | Focus | Key Milestones |
|------|-------|----------------|
| Week 1 | Research & Architecture | ATS research, tool selection, system design |
| Week 2 | Core Development | Resume parsing, NLP pipeline, basic frontend |
| Week 3 | Scoring System | Cosine Similarity, synonym dictionary, weighted scoring |
| Week 4 | Refinement & Testing | Speed optimization, feedback modules, UI polish |

---

## 📚 References

- [spaCy Documentation](https://spacy.io/usage)
- [NLTK Documentation](https://www.nltk.org/)
- [scikit-learn Cosine Similarity](https://scikit-learn.org/stable/modules/metrics.html)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Kaggle Resume Datasets](https://www.kaggle.com/datasets)
- Research papers on Resume Screening using AI

---

## 🙌 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ by <a href="https://github.com/RajGoyal01">Raj Goyal</a>
</div>
