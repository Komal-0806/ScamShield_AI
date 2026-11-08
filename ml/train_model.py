"""
ScamShield AI - Model Training Script
Trains a TF-IDF + Logistic Regression classifier on SMS/Message Scam dataset.
Evaluates accuracy, precision, recall, f1-score, and confusion matrix.
Saves model and vectorizer to models/ directory.
"""

import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_and_evaluate():
    print("=" * 60)
    print("🛡️  ScamShield AI - Machine Learning Model Training")
    print("=" * 60)

    # 1. Dataset Loading
    dataset_path = os.path.join("data", "spam_messages.csv")
    if not os.path.exists(dataset_path):
        # Fallback check for alternate naming
        alt_path = os.path.join("data", "scam_messages.csv")
        if os.path.exists(alt_path):
            dataset_path = alt_path
        else:
            raise FileNotFoundError(f"Dataset not found at {dataset_path} or {alt_path}!")

    print(f"[+] Loading dataset from: {dataset_path}")
    
    # SMS Spam collection often uses latin-1 encoding
    try:
        data = pd.read_csv(dataset_path, encoding="latin-1")
    except UnicodeDecodeError:
        data = pd.read_csv(dataset_path, encoding="utf-8", errors="replace")

    # Select the first two relevant columns (label and text)
    data = data.iloc[:, [0, 1]]
    data.columns = ["label", "message"]
    data = data.dropna()

    # Normalize labels: ham -> 0 (Legitimate), spam -> 1 (Scam/Suspicious)
    data["label"] = data["label"].astype(str).str.strip().str.lower()
    data["label"] = data["label"].map({"ham": 0, "spam": 1})
    data = data.dropna(subset=["label"])
    data["label"] = data["label"].astype(int)

    total_samples = len(data)
    ham_count = (data["label"] == 0).sum()
    spam_count = (data["label"] == 1).sum()
    print(f"[+] Total samples: {total_samples} (Legitimate: {ham_count}, Scam/Spam: {spam_count})")

    # 2. Train-Test Split (80% train, 20% test with stratification)
    X = data["message"]
    y = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
    print(f"[+] Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

    # 3. TF-IDF Feature Extraction
    # Using unigrams and bigrams with sublinear TF scaling to capture phrases like 'earn money', 'click here'
    print("[+] Extracting TF-IDF features...")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        lowercase=True,
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # 4. Train Logistic Regression Classifier
    # Balanced class weights help mitigate the class imbalance between ham and spam
    print("[+] Training Logistic Regression classifier...")
    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )
    model.fit(X_train_vec, y_train)

    # 5. Model Evaluation
    predictions = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions)
    report = classification_report(
        y_test,
        predictions,
        target_names=["Legitimate (Ham)", "Scam / Spam"]
    )

    print("\n" + "=" * 60)
    print("📊 MODEL EVALUATION RESULTS")
    print("=" * 60)
    print(f"Overall Accuracy: {accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(f"  True Negatives (Legitimate detected as Legitimate): {conf_matrix[0][0]}")
    print(f"  False Positives (Legitimate misclassified as Scam): {conf_matrix[0][1]}")
    print(f"  False Negatives (Scam missed as Legitimate):        {conf_matrix[1][0]}")
    print(f"  True Positives (Scam detected as Scam):             {conf_matrix[1][1]}")
    print("=" * 60)

    # 6. Save Model Artifacts
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "scam_model.pkl")
    vectorizer_path = os.path.join("models", "vectorizer.pkl")

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    print(f"\n[✓] Saved Model to: {model_path}")
    print(f"[✓] Saved Vectorizer to: {vectorizer_path}")
    print("[✓] Training completed successfully!\n")

if __name__ == "__main__":
    train_and_evaluate()
