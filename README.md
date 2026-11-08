# 🛡️ ScamShield AI - Digital Safety Assistant

> **Tagline:** *Think Before You Click. Stay Safe Before You Trust.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/Tests-12%20Passed-brightgreen.svg)](tests/test_scamshield.py)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**ScamShield AI** is an intelligent, privacy-preserving digital safety assistant engineered to protect citizens from modern social engineering threats, including SMS phishing (smishing), fraudulent WhatsApp employment offers, deceptive payment requests, and brand-impersonating URLs.

---

## 📌 Project Architecture

```
ScamShield AI Architecture
 ├── Input Message / Text
 │     ├── [1] TF-IDF + Logistic Regression ML Model (Statistical Pattern Recognition)
 │     ├── [2] Heuristic Red Flag Extractor (Linguistic Urgency, KYC, OTP, Lures)
 │     ├── [3] Hinglish & Vernacular Parser (Indian Cybercrime Cues)
 │     └── ➔ Hybrid Risk Score (0-100%) + Explainable Warnings + Tailored Safety Advice
 │
 ├── Input Website URL
 │     ├── Safe URL Deconstruction (Protocol, Host, Subdomain, Path)
 │     ├── Threat Indicators (Brand Impersonation, Typosquatting, Shannon Entropy, IP Host, Shorteners)
 │     └── ➔ Threat Level + Security Checklist (Safe static evaluation, zero network ping)
 │
 └── Forensic Incident Reporting (Export .TXT) & Local SQLite Storage (Emergency 1930 / cybercrime.gov.in)
```

---

## 🌟 Key Features

1. **Hybrid Message & Job Scam Detection:**
   - Evaluates SMS, WhatsApp texts, task scam offers, and fake KYC notices.
   - Combines a trained Machine Learning model with rule-based heuristics so emerging scam formats are not missed.

2. **Multilingual & Hinglish Recognition:**
   - Detects common Indian cybercrime vectors in English and Hinglish (*"Aapka bijli connection cut ho jayega"*, *"Ghar baithe kamayein"*, *"OTP share karein"*).

3. **Heuristic URL Threat Inspector:**
   - Inspects URLs without opening them to protect user security.
   - Detects **Brand Impersonation & Typosquatting** (e.g. `sbi-online-kyc.xyz` impersonating SBI, or `arnazon.top` mimicking Amazon).
   - Identifies raw IP hosts, suspicious/abused TLDs (`.xyz`, `.top`, `.buzz`, etc.), masked shorteners (`bit.ly`, `tinyurl`), and high Shannon character entropy.

4. **Explainable AI (XAI) Output:**
   - ScamShield does not just output a raw score. It lists the exact **warning signs** found (fear tactics, fake jobs, sensitive credential requests, etc.) with matched keywords.

5. **Exportable Forensic Incident Reports:**
   - One-click download of formal investigation summaries (`.txt`) complete with unique Incident IDs, risk scores, and evidence lists ready for filing at police stations or on `cybercrime.gov.in`.

6. **Interactive "Spot-the-Phish" Quiz:**
   - An engaging 3-question mini-quiz to test and demonstrate security awareness to hackathon judges.

7. **Incident Response & Safety Action Plans:**
   - Actionable guidelines based on the exact threat detected.
   - "Golden Hour" incident response guide for victims who already shared credentials or funds (dialing **1930** and freezing bank cards).

8. **Local Analysis History (SQLite):**
   - Keeps track of recent scans locally on the device with timestamps, risk ratings, and exportable CSV logs.

---

## 📊 Machine Learning Model & Genuine Evaluation

- **Algorithm:** Logistic Regression with `class_weight='balanced'`
- **Feature Extraction:** TF-IDF Vectorizer with unigrams & bigrams (`ngram_range=(1, 2)`), sublinear TF scaling
- **Dataset:** SMS Spam Collection Dataset (5,572 samples)
- **Split:** 80% Training (4,457 samples), 20% Testing (1,115 samples) with Stratification

### Real Evaluation Results:
| Metric | Legitimate (Ham) | Scam / Spam | Overall |
| :--- | :--- | :--- | :--- |
| **Accuracy** | - | - | **98.21%** |
| **Precision** | 0.99 | 0.94 | **0.98** |
| **Recall** | 0.99 | 0.92 | **0.98** |
| **F1-Score** | 0.99 | 0.93 | **0.98** |

### Confusion Matrix:
- **True Negatives:** 958 (Legitimate messages classified correctly)
- **False Positives:** 8 (Legitimate messages flagged as suspicious)
- **False Negatives:** 12 (Spam messages missed)
- **True Positives:** 137 (Scam messages flagged correctly)

### ⚠️ Honest Dataset Limitations (Academic Integrity)
The classic SMS Spam dataset consists primarily of historical text messages. While it effectively establishes linguistic baselines, modern cybercriminals use newer vectors:
- WhatsApp task scams ("Like YouTube videos and earn ₹5000/day")
- Electricity bill disconnection panic notices
- Digital Arrest law enforcement extortion

To solve this limitation, ScamShield AI implements a **Hybrid Architecture** where the ML model's probability is combined with a heuristic social engineering pattern extractor.

---

## 📂 Project Directory Structure

```
ScamShield AI/
├── app.py                      # Main Streamlit Dashboard Application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation & presentation guide
├── data/
│   ├── spam_messages.csv       # Training dataset
│   └── scamshield.db           # SQLite database for scan logs
├── ml/
│   ├── train_model.py          # ML training and evaluation script
│   └── predict.py              # Prediction & explainability engine
├── models/
│   ├── scam_model.pkl          # Serialized Logistic Regression model
│   └── vectorizer.pkl          # Serialized TF-IDF vectorizer
├── modules/
│   ├── url_checker.py          # Heuristic URL threat analysis & typosquatting
│   ├── safety.py               # Incident response & forensic report generation
│   └── database.py             # SQLite database handling & CSV exports
└── tests/
    └── test_scamshield.py      # Automated 12-test validation suite
```

---

## 🚀 Installation & Local Execution (Windows & VS Code)

### Step 1: Open Terminal in Project Directory
Open **VS Code**, go to `Terminal` -> `New Terminal`.

### Step 2: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Run the Automated Test Suite
```powershell
python -m unittest tests/test_scamshield.py
```
*Expected Output: `Ran 12 tests in ~3s ... OK`*

### Step 4: Launch the Streamlit Application
```powershell
streamlit run app.py
```
The application will launch automatically in your browser at `http://localhost:8501`.

---

## 🌐 Deployment to Streamlit Community Cloud

1. Create a GitHub repository and push your project:
   ```powershell
   git remote add origin https://github.com/<your-username>/scamshield-ai.git
   git push -u origin main
   ```
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New App"**, select your repository, set the Main file path to `app.py`, and click **"Deploy"**.

---

## 🎤 Hackathon Presentation Guide (For Judges)

1. **Problem Statement (30 seconds):**
   *"Judges, cyber fraud has shifted toward high-pressure social engineering — fake WhatsApp jobs, electricity bill disconnection panic, and digital arrest threats. Most people panic and click before thinking."*

2. **Our Solution (30 seconds):**
   *"We built ScamShield AI. It doesn't just give a blind 'spam' score. It breaks down the threat into explainable indicators: artificial urgency, brand impersonation, and credential requests, paired with immediate emergency steps like the 1930 helpline."*

3. **Live Demonstration (1 minute):**
   - Click **"Electricity Scam"** or **"Bijli Scam (Hinglish)"**: Show how it identifies the urgency tactic, KYC demand, and shortened link, computing a 75% High Risk score.
   - Click **"Download Forensic Report"**: Show the formatted incident text file ready for police reporting.
   - Click **"Suspicious URL Inspector"** and test `http://arnazon-orders-tracking.top/verify`: Show how it detects brand typosquatting (`arnazon` mimicking `amazon`) on an unauthorized `.top` domain.
   - Show the **"Spot-the-Phish Quiz"** and the **"1930 Cyber Helpline & Emergency Guide"**.
