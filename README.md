# 🛡️ ScamShield AI - Full-Stack Digital Safety Platform

> **Tagline:** *Think Before You Click. Stay Safe Before You Trust.*

[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61dafb.svg)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Netlify](https://img.shields.io/badge/Deploy-Netlify-00C7B7.svg)](https://www.netlify.com/)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7.svg)](https://render.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Logistic%20Regression-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**ScamShield AI** is an intelligent, privacy-preserving digital safety platform engineered to protect citizens from modern social engineering threats, including SMS phishing (smishing), fraudulent WhatsApp employment offers, deceptive payment requests, and brand-impersonating URLs.

---

## 📌 Full-Stack System Architecture

```
                          ┌─────────────────────────────────────┐
                          │     React + Vite Client (Netlify)   │
                          │   Premium Red-and-White SaaS Theme  │
                          └──────────────────┬──────────────────┘
                                             │ REST API (JSON)
                                             ▼
                          ┌─────────────────────────────────────┐
                          │       FastAPI Backend (Render)      │
                          │     CORS Enabled • REST Endpoints   │
                          └───────┬─────────────────────┬───────┘
                                  │                     │
                     ┌────────────▼──────────┐   ┌──────▼────────────┐
                     │ ML Classification     │   │ URL Threat Engine │
                     │ • TF-IDF Vectorizer   │   │ • Typosquatting   │
                     │ • Logistic Regression │   │ • Shannon Entropy │
                     │ • Heuristic Patterns  │   │ • Brand Spoofing  │
                     └───────────────────────┘   └───────────────────┘
```

---

## 📂 Project Directory Structure

```
ScamShield AI/
├── main.py                     # FastAPI REST API Backend server
├── render.yaml                 # Render Blueprint configuration
├── netlify.toml                # Netlify SPA build and redirect rules
├── requirements.txt            # Python dependencies (FastAPI, uvicorn, scikit-learn, etc.)
├── .gitignore                  # Git hygiene rules
│
├── frontend/                   # Modern React + Vite Web Application
│   ├── index.html              # HTML Entry Point
│   ├── package.json            # NPM dependencies (React 18, Lucide-React, Vite)
│   ├── vite.config.js          # Vite Bundler configuration
│   ├── .env                    # Local API environment (http://localhost:8000)
│   ├── .env.production         # Production API environment (Render Backend URL)
│   └── src/
│       ├── main.jsx            # React root mount
│       ├── App.jsx             # State & page routing controller
│       ├── index.css           # Premium Red-and-White Light SaaS Theme
│       └── components/
│           ├── Navbar.jsx      # Top brand header & navigation links
│           ├── Hero.jsx        # Landing hero banner, metrics & threat blueprints
│           ├── MessageChecker.jsx  # Interactive SMS & Job Scam Scanner
│           ├── UrlChecker.jsx  # Safe static URL & Typosquatting Inspector
│           ├── About.jsx       # 1930 Helpline, bank directory & Spot-the-Phish Quiz
│           ├── History.jsx     # SQLite scan activity log & CSV exporter
│           └── Footer.jsx      # Professional SaaS footer
│
├── data/
│   ├── spam_messages.csv       # 5,572 sample training dataset
│   └── scamshield.db           # SQLite database for scan logs
├── ml/
│   ├── train_model.py          # TF-IDF + Logistic Regression training script
│   └── predict.py              # Hybrid ML + Heuristic explainability engine
├── models/
│   ├── scam_model.pkl          # Serialized ML model
│   └── vectorizer.pkl          # Serialized TF-IDF feature vectorizer
├── modules/
│   ├── url_checker.py          # Heuristic URL analyzer & typosquatting logic
│   ├── safety.py               # Incident response & forensic report generator
│   └── database.py             # SQLite database operations & CSV export
└── tests/
    └── test_scamshield.py      # Automated 12-test validation suite
```

---

## 🚀 Running Locally (Full-Stack Mode)

### 1. Start the FastAPI Backend
Open your VS Code terminal and activate Python environment:
```powershell
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000
```
Backend will be live at `http://localhost:8000` (Interactive Swagger Docs at `http://localhost:8000/docs`).

### 2. Start the React Frontend
Open a second terminal:
```powershell
cd frontend
npm run dev
```
Frontend will be live at `http://localhost:5173`.

---

## 🌐 Cloud Deployment Guide

### Part 1: Deploy Backend on Render (Free)

1. Create a free account on [Render.com](https://render.com).
2. Go to **Dashboard** ➔ Click **New +** ➔ Select **Web Service** (or **Blueprint**).
3. Connect your GitHub repository (`scamshield-ai`).
4. Configure service settings:
   - **Name:** `scamshield-backend`
   - **Environment:** `Python`
   - **Region:** Any (e.g. Oregon or Frankfurt)
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Deploy Web Service**.
6. Once deployed, Render will provide your public backend URL (e.g., `https://scamshield-backend.onrender.com`).

---

### Part 2: Deploy Frontend on Netlify (Free)

1. Create a free account on [Netlify.com](https://www.netlify.com).
2. Click **Add new site** ➔ **Import an existing project** ➔ Choose **GitHub**.
3. Select your `scamshield-ai` repository.
4. Netlify will automatically detect settings from `netlify.toml`:
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/dist`
5. Under **Environment variables**, add:
   - `VITE_API_URL` = `https://scamshield-backend.onrender.com` (Your Render Backend URL from Part 1)
6. Click **Deploy scamshield-ai**.
7. Netlify will build your React application and provide your public frontend URL (e.g., `https://scamshield-ai.netlify.app`).

---

## 📊 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check and system metadata |
| `POST` | `/api/analyze-message` | Analyzes SMS/WhatsApp message, returns risk score, red flags, recommendations |
| `POST` | `/api/analyze-url` | Analyzes website URL, returns typosquatting, brand spoofing, entropy, indicators |
| `GET` | `/api/history` | Fetches recent scan activity and aggregate metrics |
| `DELETE`| `/api/history` | Clears local activity log |
| `GET` | `/api/history/export` | Exports scan history as CSV string |
| `GET` | `/api/emergency-contacts`| Returns official 1930 helpline and bank fraud numbers |

---

## 🧪 Automated Testing

Run the test suite to verify all ML predictions and heuristic rules:
```powershell
python -m unittest tests/test_scamshield.py
```
*Result: 12 tests passing in < 3s.*
