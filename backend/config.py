"""
Configuration for the AI Resume Analyser.
Contains scoring criteria, skill databases, and MNC standards.
"""

import os

# Flask config
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max

# ─────────────────────────────────────────────
# MNC STANDARDS & SCORING WEIGHTS
# ─────────────────────────────────────────────

SCORING_WEIGHTS = {
    "skills_match": 0.25,
    "experience_quality": 0.15,
    "education": 0.10,
    "projects": 0.15,
    "formatting": 0.10,
    "keywords_ats": 0.10,
    "certifications": 0.05,
    "achievements": 0.05,
    "soft_skills": 0.05,
}

# ─────────────────────────────────────────────
# DOMAIN-SPECIFIC SKILL DATABASES
# ─────────────────────────────────────────────

DOMAIN_SKILLS = {
    "Computer Science": {
        "core": [
            "data structures", "algorithms", "object oriented programming",
            "oop", "database management", "dbms", "operating systems",
            "computer networks", "software engineering", "compiler design",
            "theory of computation", "discrete mathematics", "computer architecture",
        ],
        "programming": [
            "python", "java", "c++", "c", "javascript", "typescript",
            "go", "rust", "kotlin", "swift", "ruby", "php", "scala",
            "r", "matlab", "sql", "html", "css",
        ],
        "frameworks": [
            "react", "angular", "vue", "django", "flask", "spring boot",
            "node.js", "express", "fastapi", "next.js", "tensorflow",
            "pytorch", "keras", "scikit-learn", "pandas", "numpy",
            ".net", "asp.net", "laravel", "rails",
        ],
        "technologies": [
            "docker", "kubernetes", "aws", "azure", "gcp", "git",
            "linux", "ci/cd", "jenkins", "terraform", "ansible",
            "redis", "mongodb", "postgresql", "mysql", "elasticsearch",
            "kafka", "rabbitmq", "graphql", "rest api", "microservices",
            "machine learning", "deep learning", "artificial intelligence",
            "natural language processing", "computer vision", "blockchain",
            "cloud computing", "devops", "agile", "scrum",
        ],
    },
    "Electrical Engineering": {
        "core": [
            "circuit analysis", "analog electronics", "digital electronics",
            "signals and systems", "control systems", "power systems",
            "electromagnetic theory", "electrical machines", "power electronics",
            "microprocessors", "vlsi", "communication systems",
        ],
        "programming": [
            "matlab", "simulink", "python", "c", "c++", "verilog",
            "vhdl", "labview", "assembly",
        ],
        "frameworks": [
            "arduino", "raspberry pi", "cadence", "ltspice",
            "proteus", "multisim", "altium designer", "eagle",
        ],
        "technologies": [
            "pcb design", "embedded systems", "iot", "plc",
            "scada", "renewable energy", "solar energy", "wind energy",
            "smart grid", "automation", "robotics", "sensor technology",
        ],
    },
    "Mechanical Engineering": {
        "core": [
            "thermodynamics", "fluid mechanics", "heat transfer",
            "strength of materials", "machine design", "manufacturing processes",
            "engineering mechanics", "kinematics", "dynamics",
            "vibrations", "finite element analysis",
        ],
        "programming": [
            "matlab", "python", "c", "c++", "fortran",
        ],
        "frameworks": [
            "solidworks", "autocad", "catia", "ansys", "abaqus",
            "creo", "fusion 360", "inventor", "nx siemens",
        ],
        "technologies": [
            "3d printing", "additive manufacturing", "cad", "cam", "cae",
            "cfd", "fea", "robotics", "automation", "iot",
            "lean manufacturing", "six sigma", "quality control",
        ],
    },
    "Civil Engineering": {
        "core": [
            "structural analysis", "structural design", "geotechnical engineering",
            "fluid mechanics", "hydraulics", "surveying",
            "construction management", "transportation engineering",
            "environmental engineering", "soil mechanics",
        ],
        "programming": [
            "matlab", "python", "r",
        ],
        "frameworks": [
            "autocad", "revit", "staad pro", "etabs", "sap2000",
            "primavera", "ms project", "civil 3d", "tekla",
        ],
        "technologies": [
            "bim", "gis", "remote sensing", "green building",
            "sustainable construction", "project management",
            "cost estimation", "quality management",
        ],
    },
    "Data Science": {
        "core": [
            "statistics", "probability", "linear algebra",
            "machine learning", "deep learning", "data mining",
            "data analysis", "data visualization", "big data",
            "natural language processing", "computer vision",
        ],
        "programming": [
            "python", "r", "sql", "scala", "julia", "java",
        ],
        "frameworks": [
            "tensorflow", "pytorch", "keras", "scikit-learn",
            "pandas", "numpy", "matplotlib", "seaborn", "plotly",
            "spark", "hadoop", "airflow", "dbt",
        ],
        "technologies": [
            "aws", "azure", "gcp", "docker", "kubernetes",
            "tableau", "power bi", "looker", "mlflow",
            "databricks", "snowflake", "redshift", "bigquery",
            "a/b testing", "feature engineering", "model deployment",
        ],
    },
    "Electronics & Communication": {
        "core": [
            "analog electronics", "digital electronics", "signals and systems",
            "communication systems", "digital signal processing",
            "microprocessors", "microcontrollers", "vlsi design",
            "electromagnetic theory", "antenna design", "control systems",
        ],
        "programming": [
            "c", "c++", "python", "matlab", "verilog", "vhdl",
            "assembly", "embedded c",
        ],
        "frameworks": [
            "arduino", "raspberry pi", "cadence", "xilinx",
            "keil", "stm32", "esp32",
        ],
        "technologies": [
            "pcb design", "embedded systems", "iot", "wireless communication",
            "5g", "rf design", "fpga", "asic", "signal processing",
            "image processing", "radar systems",
        ],
    },
    "MBA / Business": {
        "core": [
            "financial analysis", "marketing management", "operations management",
            "human resource management", "strategic management",
            "organizational behavior", "business analytics",
            "supply chain management", "project management",
        ],
        "programming": [
            "excel", "sql", "python", "r", "vba",
        ],
        "frameworks": [
            "sap", "salesforce", "hubspot", "jira", "asana",
            "power bi", "tableau",
        ],
        "technologies": [
            "crm", "erp", "digital marketing", "seo", "sem",
            "social media marketing", "content marketing",
            "market research", "business intelligence",
            "lean management", "six sigma", "agile",
        ],
    },
}

# ─────────────────────────────────────────────
# MNC-LEVEL EXPECTATIONS (for scoring context)
# ─────────────────────────────────────────────

MNC_STANDARDS = {
    "Google": {
        "focus": ["algorithms", "data structures", "system design", "problem solving"],
        "min_skills": 8, "projects_expected": 3, "certifications_bonus": True,
        "tier": 1, "min_score": 75, "domains": ["Computer Science", "Data Science"],
        "hiring_bar": "Very High", "emoji": "🔵",
    },
    "Microsoft": {
        "focus": ["c++", "c#", "azure", "system design", "algorithms"],
        "min_skills": 7, "projects_expected": 3, "certifications_bonus": True,
        "tier": 1, "min_score": 70, "domains": ["Computer Science", "Data Science"],
        "hiring_bar": "Very High", "emoji": "🟢",
    },
    "Amazon": {
        "focus": ["aws", "system design", "data structures", "leadership principles"],
        "min_skills": 8, "projects_expected": 3, "certifications_bonus": True,
        "tier": 1, "min_score": 70, "domains": ["Computer Science", "Data Science"],
        "hiring_bar": "Very High", "emoji": "🟠",
    },
    "Meta": {
        "focus": ["algorithms", "react", "system design", "scalability"],
        "min_skills": 7, "projects_expected": 3, "certifications_bonus": True,
        "tier": 1, "min_score": 75, "domains": ["Computer Science", "Data Science"],
        "hiring_bar": "Very High", "emoji": "🔵",
    },
    "Apple": {
        "focus": ["swift", "objective-c", "system design", "ui/ux"],
        "min_skills": 7, "projects_expected": 3, "certifications_bonus": True,
        "tier": 1, "min_score": 72, "domains": ["Computer Science", "Electronics & Communication"],
        "hiring_bar": "Very High", "emoji": "⚪",
    },
    "Netflix": {
        "focus": ["system design", "microservices", "java", "scalability"],
        "min_skills": 8, "projects_expected": 3, "certifications_bonus": True,
        "tier": 1, "min_score": 78, "domains": ["Computer Science", "Data Science"],
        "hiring_bar": "Extremely High", "emoji": "🔴",
    },
    "Adobe": {
        "focus": ["javascript", "react", "algorithms", "ui/ux", "machine learning"],
        "min_skills": 7, "projects_expected": 3, "certifications_bonus": True,
        "tier": 1, "min_score": 65, "domains": ["Computer Science", "Data Science"],
        "hiring_bar": "High", "emoji": "🔴",
    },
    "Salesforce": {
        "focus": ["java", "cloud computing", "rest api", "sql", "agile"],
        "min_skills": 6, "projects_expected": 2, "certifications_bonus": True,
        "tier": 1, "min_score": 60, "domains": ["Computer Science", "MBA / Business"],
        "hiring_bar": "High", "emoji": "☁️",
    },
    "Goldman Sachs": {
        "focus": ["java", "python", "algorithms", "data structures", "sql"],
        "min_skills": 7, "projects_expected": 2, "certifications_bonus": True,
        "tier": 1, "min_score": 68, "domains": ["Computer Science", "Data Science", "MBA / Business"],
        "hiring_bar": "Very High", "emoji": "💰",
    },
    "Deloitte": {
        "focus": ["python", "sql", "cloud computing", "agile", "project management"],
        "min_skills": 5, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 55, "domains": ["Computer Science", "Data Science", "MBA / Business"],
        "hiring_bar": "Medium-High", "emoji": "🟢",
    },
    "Accenture": {
        "focus": ["java", "cloud computing", "agile", "devops", "sql"],
        "min_skills": 5, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 50, "domains": ["Computer Science", "Data Science", "MBA / Business", "Electrical Engineering", "Electronics & Communication", "Mechanical Engineering"],
        "hiring_bar": "Medium", "emoji": "🟣",
    },
    "Capgemini": {
        "focus": ["java", "python", "sql", "cloud computing", "agile"],
        "min_skills": 5, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 48, "domains": ["Computer Science", "Data Science", "Electronics & Communication", "Electrical Engineering"],
        "hiring_bar": "Medium", "emoji": "🔵",
    },
    "Cognizant": {
        "focus": ["java", "python", "sql", "agile"],
        "min_skills": 4, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 45, "domains": ["Computer Science", "Data Science", "Electronics & Communication", "Electrical Engineering", "Mechanical Engineering"],
        "hiring_bar": "Medium", "emoji": "🔷",
    },
    "TCS": {
        "focus": ["java", "python", "sql", "agile", "problem solving"],
        "min_skills": 5, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 40, "domains": ["Computer Science", "Data Science", "Electrical Engineering", "Electronics & Communication", "Mechanical Engineering", "Civil Engineering"],
        "hiring_bar": "Medium", "emoji": "🟦",
    },
    "Infosys": {
        "focus": ["java", "python", "sql", "cloud computing"],
        "min_skills": 5, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 42, "domains": ["Computer Science", "Data Science", "Electrical Engineering", "Electronics & Communication", "Mechanical Engineering", "Civil Engineering"],
        "hiring_bar": "Medium", "emoji": "🟦",
    },
    "Wipro": {
        "focus": ["java", "python", "sql", "devops"],
        "min_skills": 5, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 40, "domains": ["Computer Science", "Data Science", "Electrical Engineering", "Electronics & Communication", "Mechanical Engineering", "Civil Engineering"],
        "hiring_bar": "Medium", "emoji": "🌸",
    },
    "HCLTech": {
        "focus": ["java", "python", "sql", "devops", "cloud computing"],
        "min_skills": 5, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 42, "domains": ["Computer Science", "Data Science", "Electronics & Communication", "Electrical Engineering"],
        "hiring_bar": "Medium", "emoji": "🟦",
    },
    "Tech Mahindra": {
        "focus": ["java", "python", "sql", "networking"],
        "min_skills": 4, "projects_expected": 2, "certifications_bonus": True,
        "tier": 3, "min_score": 38, "domains": ["Computer Science", "Electronics & Communication", "Electrical Engineering", "Mechanical Engineering"],
        "hiring_bar": "Moderate", "emoji": "🔷",
    },
    "L&T Infotech": {
        "focus": ["java", "python", "sql", "project management"],
        "min_skills": 4, "projects_expected": 2, "certifications_bonus": True,
        "tier": 3, "min_score": 38, "domains": ["Computer Science", "Civil Engineering", "Mechanical Engineering", "Electrical Engineering"],
        "hiring_bar": "Moderate", "emoji": "🏗️",
    },
    "Bosch": {
        "focus": ["embedded systems", "c", "c++", "iot", "automation"],
        "min_skills": 5, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 50, "domains": ["Electronics & Communication", "Electrical Engineering", "Mechanical Engineering", "Computer Science"],
        "hiring_bar": "Medium-High", "emoji": "🔧",
    },
    "Siemens": {
        "focus": ["automation", "plc", "scada", "python", "embedded systems"],
        "min_skills": 5, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 50, "domains": ["Electrical Engineering", "Electronics & Communication", "Mechanical Engineering"],
        "hiring_bar": "Medium-High", "emoji": "⚡",
    },
    "Tata Motors": {
        "focus": ["machine design", "cad", "manufacturing processes", "quality control"],
        "min_skills": 4, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 45, "domains": ["Mechanical Engineering", "Electrical Engineering"],
        "hiring_bar": "Medium", "emoji": "🚗",
    },
    "L&T Construction": {
        "focus": ["structural design", "project management", "autocad", "surveying"],
        "min_skills": 4, "projects_expected": 2, "certifications_bonus": True,
        "tier": 2, "min_score": 45, "domains": ["Civil Engineering", "Mechanical Engineering"],
        "hiring_bar": "Medium", "emoji": "🏗️",
    },
    "McKinsey": {
        "focus": ["strategic management", "business analytics", "financial analysis", "project management"],
        "min_skills": 5, "projects_expected": 2, "certifications_bonus": True,
        "tier": 1, "min_score": 72, "domains": ["MBA / Business"],
        "hiring_bar": "Very High", "emoji": "💼",
    },
}

# ─────────────────────────────────────────────
# RESUME SECTION KEYWORDS (for section detection)
# ─────────────────────────────────────────────

SECTION_KEYWORDS = {
    "education": [
        "education", "academic", "qualification", "degree", "university",
        "college", "school", "institute", "coursework", "gpa", "cgpa",
    ],
    "experience": [
        "experience", "work history", "employment", "professional experience",
        "internship", "work experience", "career",
    ],
    "skills": [
        "skills", "technical skills", "core competencies", "technologies",
        "proficiencies", "expertise", "tools", "languages",
    ],
    "projects": [
        "projects", "personal projects", "academic projects",
        "key projects", "notable projects",
    ],
    "certifications": [
        "certifications", "certificates", "licenses", "credentials",
        "professional development", "courses",
    ],
    "achievements": [
        "achievements", "awards", "honors", "recognition",
        "accomplishments", "publications",
    ],
    "summary": [
        "summary", "objective", "profile", "about me",
        "professional summary", "career objective",
    ],
}

# ─────────────────────────────────────────────
# SOFT SKILLS DATABASE
# ─────────────────────────────────────────────

SOFT_SKILLS = [
    "leadership", "communication", "teamwork", "collaboration",
    "problem solving", "critical thinking", "analytical",
    "time management", "adaptability", "creativity",
    "interpersonal", "presentation", "mentoring",
    "negotiation", "decision making", "conflict resolution",
    "emotional intelligence", "work ethic", "attention to detail",
    "self motivated", "proactive", "organized",
]

# ─────────────────────────────────────────────
# ACTION VERBS (strong resume language)
# ─────────────────────────────────────────────

ACTION_VERBS = [
    "achieved", "accomplished", "administered", "advanced", "analyzed",
    "architected", "automated", "built", "collaborated", "conducted",
    "created", "decreased", "delivered", "designed", "developed",
    "devised", "directed", "drove", "eliminated", "engineered",
    "established", "executed", "expanded", "facilitated", "founded",
    "generated", "grew", "headed", "implemented", "improved",
    "increased", "initiated", "innovated", "integrated", "introduced",
    "launched", "led", "managed", "maximized", "mentored",
    "minimized", "optimized", "orchestrated", "organized", "overhauled",
    "pioneered", "planned", "produced", "programmed", "published",
    "redesigned", "reduced", "refactored", "resolved", "revamped",
    "scaled", "simplified", "spearheaded", "streamlined", "supervised",
    "transformed", "upgraded",
]

# ─────────────────────────────────────────────
# COURSES (for dropdown options)
# ─────────────────────────────────────────────

COURSES = [
    "B.Tech", "M.Tech", "B.E.", "M.E.", "BCA", "MCA",
    "B.Sc", "M.Sc", "MBA", "BBA", "Ph.D",
    "Diploma", "B.Com", "M.Com", "BA", "MA",
]

BRANCHES = [
    "Computer Science",
    "Data Science",
    "Electrical Engineering",
    "Electronics & Communication",
    "Mechanical Engineering",
    "Civil Engineering",
    "MBA / Business",
]
