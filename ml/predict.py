"""
ScamShield AI - Message Prediction & Explainability Engine
Combines TF-IDF Logistic Regression ML model with multilingual heuristic extraction
for explainable scam, smishing, job fraud, and social engineering detection.
"""

import os
import re
import joblib

MODEL_PATH = os.path.join("models", "scam_model.pkl")
VECTORIZER_PATH = os.path.join("models", "vectorizer.pkl")

# Cached model and vectorizer instances
_model = None
_vectorizer = None

def load_prediction_model():
    """Loads the serialized model and vectorizer if not already loaded."""
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            raise FileNotFoundError(
                "Model files not found! Please run 'python ml/train_model.py' first."
            )
        _model = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VECTORIZER_PATH)
    return _model, _vectorizer

# Comprehensive Heuristic Patterns (English + Hinglish / Vernacular Indian Cues)
HEURISTIC_PATTERNS = {
    "urgency": {
        "title": "Artificial Urgency & Fear Tactics",
        "title_hi": "कृत्रिम तात्कालिकता और भय (Urgency & Fear)",
        "pattern": r"(immediately|urgent|hurry|act now|expires?|suspended|blocked|disconnected|within \d+ (?:hours?|mins?)|last chance|today only|immediate action|turant|aaj hi|jaldi|khatra|band ho jayega|rok diya gaya|aaj raat|block kar diya|disconnect ho jayega)",
        "weight": 20,
        "description": "Scammers create artificial panic with countdowns or immediate threats to force hasty decisions."
    },
    "sensitive_info": {
        "title": "Request for Sensitive Credentials / KYC",
        "title_hi": "गोपनीय विवरण / KYC की मांग",
        "pattern": r"(otp|password|pin\b|cvv|aadhaar|pan card|kyc|verify your account|bank details|credit card|debit card|net banking|khata number|khate me|pan update|aadhaar link|bank vivaran)",
        "weight": 30,
        "description": "Legitimate institutions and banks never request confidential OTPs, passwords, or PINs via text message or chat."
    },
    "financial_lure": {
        "title": "Unrealistic Financial Rewards or Lottery",
        "title_hi": "अवास्तविक लॉटरी या नकद पुरस्कार का लालच",
        "pattern": r"(won\b|winner|lottery|prize|jackpot|cashback|free gift|reward points|claim ₹?\d+|credited|bonus|refund|guaranteed returns|crypto airdrop|inam jeeta|lakhpati|muft upahar|bina kisi kharch|paisa mila)",
        "weight": 25,
        "description": "Promises of free money, lottery winnings, or unexpected cashbacks are hallmarks of financial fraud."
    },
    "fake_jobs": {
        "title": "Suspicious / Fake Job Offer Indicators",
        "title_hi": "फर्जी नौकरी / पार्ट-टाइम टास्क फ्रॉड",
        "pattern": r"(part[- ]time|work from home|daily (?:pay|payout|income|salary|earn)|earn (?:₹|\$|rs\.?|inr)?\s*\d+|review task|telegram hr|contact hr|like (?:youtube|videos)|subscribe channel|rating task|no experience|ghar baithe|kamayein|rojana|rozana|part time kaam|video like karein|hotel review)",
        "weight": 25,
        "description": "Part-time job offers offering exorbitant daily pay for simple tasks (like liking videos) are known task scams."
    },
    "upi_qr_fraud": {
        "title": "Deceptive UPI / Payment Trap",
        "title_hi": "धोखाधड़ी वाली UPI / QR कोड भुगतान मांग",
        "pattern": r"(scan qr|send ₹?1 to (?:verify|receive)|enter upi pin to receive|collect request|paytm kyc|gpay cashback)",
        "weight": 30,
        "description": "Entering your UPI PIN always sends money; it is never required to receive money."
    },
    "digital_arrest_extortion": {
        "title": "Impersonation of Law Enforcement / Digital Arrest",
        "title_hi": "पुलिस / CBI अधिकारी बनकर धमकी",
        "pattern": r"(digital arrest|cbi officer|police department|narcotics bureau|customs seizure|illegal parcel|fir registered|arrest warrant|court summons|cyber crime cell)",
        "weight": 35,
        "description": "Law enforcement agencies never conduct 'digital arrests' over video calls or demand money to settle cases."
    },
    "suspicious_links": {
        "title": "Unverified or Shortened Links / Direct Redirect",
        "title_hi": "संदेहास्पद लिंक या APK डाउनलोड फ़ाइल",
        "pattern": r"(https?://\S+|bit\.ly/\S+|tinyurl\.com/\S+|t\.me/\S+|wa\.me/\S+|chat\.whatsapp\.com/\S+|\b\S+\.apk\b)",
        "weight": 20,
        "description": "Direct links to URL shorteners, messaging apps, or APK download files bypass normal app store security."
    },
    "courier_utility": {
        "title": "Utility / Courier Delivery Scam Cues",
        "title_hi": "बिजली बिल / पार्सल डिलीवरी फ्रॉड",
        "pattern": r"(electricity bill|power (?:cut|disconnection)|courier|parcel|delivery failed|customs duty|update address|traffic challan|speed post|bijli bill|light bill|parcel ruka|dak vibhag|challan bharein)",
        "weight": 20,
        "description": "Impersonates postal services, electricity boards, or traffic police claiming pending dues or delivery failure."
    }
}

def detect_language(text: str) -> str:
    """Detects whether text has Hinglish / Hindi cues or standard English."""
    hinglish_markers = [
        "aapka", "karein", "turant", "aaj", "paisa", "inam", "bijli", "ghar",
        "kamayein", "khata", "bina", "mila", "karo", "nahi", "raat"
    ]
    text_lower = text.lower()
    matches = sum(1 for word in hinglish_markers if re.search(rf"\b{word}\b", text_lower))
    return "Hinglish / Hindi" if matches >= 2 else "English"

def extract_red_flags(text: str):
    """
    Scans the message for explainable red flags using regex heuristics.
    Returns detected flags list and heuristic score.
    """
    flags_detected = []
    heuristic_score = 0
    matched_words = []

    text_lower = text.lower()

    for category, meta in HEURISTIC_PATTERNS.items():
        matches = re.findall(meta["pattern"], text_lower, flags=re.IGNORECASE)
        if matches:
            extracted = []
            for m in matches:
                if isinstance(m, tuple):
                    extracted.extend([x.strip() for x in m if x and len(x.strip()) > 1])
                else:
                    extracted.append(m.strip())
            
            clean_matches = list(dict.fromkeys(extracted))[:3]
            matched_words.extend(clean_matches)
            
            flags_detected.append({
                "category": meta["title"],
                "category_hi": meta["title_hi"],
                "description": meta["description"],
                "matches": clean_matches
            })
            heuristic_score += meta["weight"]

    # Cap heuristic score at 100
    heuristic_score = min(heuristic_score, 100)
    return flags_detected, heuristic_score, list(dict.fromkeys(matched_words))

def predict_message(text: str) -> dict:
    """
    Analyzes an input message using both the trained ML model and heuristic explainability rules.
    Returns a comprehensive result dictionary.
    """
    if not text or not text.strip():
        return {
            "error": "Empty message provided. Please enter text to analyze."
        }

    clean_text = text.strip()
    model, vectorizer = load_prediction_model()
    detected_lang = detect_language(clean_text)

    # 1. ML Model Prediction & Probability
    text_vec = vectorizer.transform([clean_text])
    probabilities = model.predict_proba(text_vec)[0]
    # Class 0: Ham/Legitimate, Class 1: Scam/Spam
    ml_scam_prob = float(probabilities[1]) * 100

    # 2. Heuristic Analysis & Red Flags
    red_flags, heuristic_score, detected_terms = extract_red_flags(clean_text)

    # 3. Hybrid Risk Score (Combines ML + Heuristics)
    flag_titles = [f["category"] for f in red_flags]
    if heuristic_score > 0:
        combined_score = (0.50 * ml_scam_prob) + (0.50 * heuristic_score)

        # High-severity rule floors for severe threats
        if "Impersonation of Law Enforcement / Digital Arrest" in flag_titles:
            combined_score = max(combined_score, 88.0)
        elif "Deceptive UPI / Payment Trap" in flag_titles:
            combined_score = max(combined_score, 85.0)
        elif "Request for Sensitive Credentials / KYC" in flag_titles:
            combined_score = max(combined_score, 75.0)
        elif "Suspicious / Fake Job Offer Indicators" in flag_titles and "Unverified or Shortened Links / Direct Redirect" in flag_titles:
            combined_score = max(combined_score, 80.0)
    else:
        combined_score = ml_scam_prob

    combined_score = round(min(max(combined_score, 0.0), 100.0), 1)

    # 4. Determine Verdict & Risk Tier
    if combined_score >= 65.0:
        risk_level = "High Risk"
        verdict = "Likely Scam / Fraudulent"
        theme_color = "red"
    elif combined_score >= 35.0:
        risk_level = "Moderate Risk"
        verdict = "Suspicious (Exercise Caution)"
        theme_color = "orange"
    else:
        risk_level = "Low Risk"
        verdict = "Likely Legitimate"
        theme_color = "green"

    return {
        "verdict": verdict,
        "risk_level": risk_level,
        "risk_score": combined_score,
        "ml_probability": round(ml_scam_prob, 1),
        "heuristic_score": heuristic_score,
        "red_flags": red_flags,
        "flag_count": len(red_flags),
        "detected_terms": detected_terms,
        "theme_color": theme_color,
        "language": detected_lang
    }

if __name__ == "__main__":
    test_samples = [
        "Hey Mom, are we still meeting for lunch at 1 PM tomorrow?",
        "Dear customer, your SBI account KYC is expired. Power disconnected tonight. Call immediately or click bit.ly/sbi-kyc",
        "Aapka bijli connection aaj raat 9:30 baje disconnect ho jayega. Turant kyc update karein bit.ly/bijli-pay",
        "Digital Arrest Warning: CBI officer speaking. Your parcel containing illegal narcotics seized at customs. Join Skype call immediately or face arrest warrant.",
        "Amazon Part-Time Hiring! Earn ₹3000 to ₹8000 daily by liking YouTube videos. Contact HR on WhatsApp: wa.me/9199999999"
    ]

    print("Running Predictor Test Cases:\n" + "=" * 55)
    for sample in test_samples:
        result = predict_message(sample)
        print(f"Message: {sample[:60]}... [{result['language']}]")
        print(f"Verdict: {result['verdict']} | Risk Score: {result['risk_score']}% | Red Flags: {result['flag_count']}")
        for flag in result['red_flags']:
            print(f"  - [{flag['category']}]: {flag['description']} (Matches: {flag['matches']})")
        print("-" * 55)
