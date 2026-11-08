"""
ScamShield AI - Comprehensive Automated Test Suite
Verifies ML model, heuristic rules, URL threat detection, and SQLite database.
"""

import os
import unittest
from ml.predict import predict_message, load_prediction_model
from modules.url_checker import analyze_url, detect_brand_impersonation, calculate_shannon_entropy
from modules.safety import get_message_recommendations, get_url_recommendations, generate_incident_report
from modules.database import add_scan_record, get_recent_scans, get_scan_statistics, export_history_as_csv

class TestScamShield(unittest.TestCase):

    def test_01_model_loading(self):
        """Test model and vectorizer load without error."""
        model, vectorizer = load_prediction_model()
        self.assertIsNotNone(model)
        self.assertIsNotNone(vectorizer)

    def test_02_legitimate_message(self):
        """Test legitimate messages receive low risk scores."""
        msg = "Hi Dad, I will reach home by 7 PM today. Let me know if you need anything from the store."
        res = predict_message(msg)
        self.assertEqual(res["risk_level"], "Low Risk")
        self.assertLess(res["risk_score"], 35.0)
        self.assertEqual(res["flag_count"], 0)

    def test_03_electricity_bill_scam(self):
        """Test electricity bill scam detection."""
        msg = "Dear consumer your electricity power will be disconnected tonight at 9:30 PM. Call officer at 9876543210 immediately or update KYC at bit.ly/power-bill"
        res = predict_message(msg)
        self.assertIn(res["risk_level"], ["High Risk", "Moderate Risk"])
        self.assertGreaterEqual(res["risk_score"], 60.0)
        categories = [f["category"] for f in res["red_flags"]]
        self.assertIn("Artificial Urgency & Fear Tactics", categories)

    def test_04_hinglish_detection(self):
        """Test detection of Hinglish vernacular scam text."""
        msg = "Aapka bijli connection aaj raat 9:30 baje disconnect ho jayega. Turant apna bill bharein aur KYC update karein: bit.ly/bijli-pay"
        res = predict_message(msg)
        self.assertEqual(res["language"], "Hinglish / Hindi")
        self.assertEqual(res["risk_level"], "High Risk")

    def test_05_fake_job_offer(self):
        """Test fake part-time YouTube job detection."""
        msg = "Part-Time Work from Home Opportunity! Earn ₹3000 to ₹7000 daily by liking YouTube videos. Contact HR on WhatsApp: wa.me/9199999999"
        res = predict_message(msg)
        self.assertEqual(res["risk_level"], "High Risk")
        categories = [f["category"] for f in res["red_flags"]]
        self.assertIn("Suspicious / Fake Job Offer Indicators", categories)

    def test_06_digital_arrest(self):
        """Test digital arrest extortion detection."""
        msg = "Digital Arrest Notice: CBI officer speaking. Your courier parcel containing narcotics seized. Join Skype immediately or face arrest warrant."
        res = predict_message(msg)
        self.assertEqual(res["risk_level"], "High Risk")
        categories = [f["category"] for f in res["red_flags"]]
        self.assertIn("Impersonation of Law Enforcement / Digital Arrest", categories)

    def test_07_safe_url(self):
        """Test legitimate official websites are scored safe."""
        url = "https://www.google.com/search?q=cybersecurity"
        res = analyze_url(url)
        self.assertEqual(res["risk_level"], "Low Risk")
        self.assertEqual(res["risk_score"], 0)

    def test_08_brand_impersonation_url(self):
        """Test brand impersonation on unauthorized TLD."""
        url = "http://sbi-online-kyc-update.xyz/login.php"
        res = analyze_url(url)
        self.assertEqual(res["risk_level"], "High Risk")
        self.assertGreaterEqual(res["risk_score"], 70)
        self.assertIn("SBI", res["impersonations"])

    def test_09_typosquatting_url(self):
        """Test brand typosquatting detection."""
        url = "http://arnazon-orders-tracking.top/verify"
        res = analyze_url(url)
        self.assertEqual(res["risk_level"], "High Risk")
        self.assertIn("AMAZON", res["impersonations"])

    def test_10_raw_ip_url(self):
        """Test raw IP address detection in URL."""
        url = "http://192.168.1.100/verify-account"
        res = analyze_url(url)
        self.assertTrue(res["is_ip"])
        self.assertEqual(res["risk_level"], "High Risk")

    def test_11_incident_report_generation(self):
        """Test forensic incident report formatting."""
        msg = "Your SBI account is blocked. Call immediately."
        res = predict_message(msg)
        recs = get_message_recommendations(res)
        report = generate_incident_report("Message", msg, res, recs)
        self.assertIn("SCAMSHIELD-", report)
        self.assertIn("FORENSIC INCIDENT INVESTIGATION REPORT", report)
        self.assertIn("1930", report)

    def test_12_database_operations(self):
        """Test SQLite record storage and CSV export."""
        add_scan_record("Message", "Automated test message", 85.0, "High Risk", "Likely Scam", 2)
        stats = get_scan_statistics()
        self.assertGreater(stats["total_scans"], 0)
        csv_out = export_history_as_csv()
        self.assertIn("Automated test message", csv_out)

if __name__ == "__main__":
    unittest.main()
