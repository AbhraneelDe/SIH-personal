# SkillPassport — AI-Powered Student Skill Passport & Opportunity Matching Platform

> **"Turn Your Learning Into Opportunity."**

SkillPassport is a production-quality, high-scale web platform built with **Django 5.x + Django REST Framework + Bootstrap 5 SaaS UI + Explainable Recommendation Engine**.

---

## 🌟 Key Features

1. **Portable Skill Passport (`/passport/alex_morgan`)**:
   - Converts coursework, GitHub repositories, hackathons, and certifications into a shareable digital passport with printable PDF export support.
2. **Explainable & Fair Matching Engine**:
   - Scores opportunities transparently using weighted metrics:
     - **Skill Coverage (40%)**
     - **Evidence Verification Strength (25%)**
     - **Project Relevance (15%)**
     - **Experience Alignment (10%)**
     - **Credential Relevance (10%)**
   - **Fairness Guarantee**: Excludes age, gender, race, religion, photo, or protected attributes from recommendations.
3. **Skill Gap Analysis**:
   - Matrix showing required vs current evidence with priority indicators and recommended learning actions.
4. **Multidisciplinary Team Builder**:
   - Recommends complementary teammates for hackathons and projects based on missing skill categories.
5. **17 Realistic Pre-Loaded Demo Opportunities**:
   - Spans AI/ML Engineering, Full Stack, Python Backend, Data Science, Cloud Engineering, Cybersecurity, DevOps, and Open Source.
6. **Recruiter Portal**:
   - Opportunity posting wizard and applicant evidence inspection.

---

## 🚀 Quick Start Instructions

### 1. Database Migrations & Data Seeding
Run the following commands in terminal:

```bash
python manage.py makemigrations accounts profiles skills evidence opportunities matching teams applications notifications analytics recruiters api
python manage.py migrate
python manage.py seed_data
```

### 2. Run Development Server
```bash
python manage.py runserver 8000
```

Access the platform in your browser at `http://127.0.0.1:8000/`.

---

## 🔑 Demo Accounts

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Student** | `alex_morgan` | `password123` | Pre-loaded verified Python, ML, Cloud evidence |
| **Recruiter** | `recruiter_techcorp` | `password123` | TechCorp AI Lead Recruiter |
| **Admin** | `admin` | `password123` | Django Admin Superuser (`/admin/`) |

---

## 🧪 Automated Tests
Run unit and integration tests:

```bash
python manage.py test
```

---

## 🛠 Tech Stack
- **Backend**: Python 3.12+, Django 5.x, Django REST Framework, PostgreSQL / SQLite
- **Frontend**: HTML5, Modern CSS Custom Properties (Dark/Light SaaS theme), Bootstrap 5, FontAwesome 6, Chart.js
- **API**: REST API Endpoints at `/api/v1/`
