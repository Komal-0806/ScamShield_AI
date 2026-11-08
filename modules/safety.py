"""
ScamShield AI - Safety Recommendations, Incident Response & Forensic Reporting
Provides contextual guidance, emergency action plans, bank fraud contacts,
and formal incident report generation for cybercrime filings.
"""

from datetime import datetime
import uuid

# Official 24x7 Emergency Contact Numbers for Major Financial Institutions (India)
BANK_EMERGENCY_CONTACTS = {
    "State Bank of India (SBI)": {"toll_free": "1800 1234 / 1800 2100", "sms_block": "SMS 'BLOCK <card_last_4>' to 567676"},
    "HDFC Bank": {"toll_free": "1800 202 6161 / 1800 1600", "sms_block": "Use MobileBanking or netbanking portal"},
    "ICICI Bank": {"toll_free": "1800 1080", "sms_block": "SMS 'BLOCK <account_number>' to 9215676766"},
    "Axis Bank": {"toll_free": "1860 419 5555 / 1860 500 5555", "sms_block": "SMS 'BLOCK <card_no>' to 56161600"},
    "Punjab National Bank (PNB)": {"toll_free": "1800 1800 / 1800 2021", "sms_block": "SMS 'HOTLIST' to 5607040"}
}

def get_message_recommendations(analysis: dict) -> list:
    """
    Returns specific, prioritized safety recommendations based on the message analysis results.
    """
    recommendations = []
    risk_level = analysis.get("risk_level", "Low Risk")
    red_flags = analysis.get("red_flags", [])
    categories = [f["category"] for f in red_flags]

    # Universal High/Moderate Risk Warnings
    if risk_level == "High Risk":
        recommendations.append({
            "action": "Do Not Engage or Reply",
            "priority": "Urgent",
            "details": "Do not reply to the sender, confirm your identity, or click any embedded buttons/links. Engaging confirms your number is active."
        })
    elif risk_level == "Moderate Risk":
        recommendations.append({
            "action": "Proceed With Caution & Independent Verification",
            "priority": "High",
            "details": "Do not use contact numbers or links provided in this message. Find the organization's official website independently."
        })

    # Digital Arrest / Extortion Alert
    if "Impersonation of Law Enforcement / Digital Arrest" in categories:
        recommendations.append({
            "action": "Disconnect Immediately - Digital Arrest is Fake",
            "priority": "Critical",
            "details": "Indian law enforcement (Police, CBI, ED, Narcotics) NEVER arrests citizens over Skype, WhatsApp, or video calls. Do not pay any 'clearance fee' or 'bond'."
        })

    # Deceptive UPI PIN Trap
    if "Deceptive UPI / Payment Trap" in categories:
        recommendations.append({
            "action": "Never Enter UPI PIN to Receive Money",
            "priority": "Critical",
            "details": "UPI PIN is required ONLY to debit money from your account. Receiving payments or cashbacks never requires scanning a QR code or entering your PIN."
        })

    # Sensitive Info / KYC Request
    if "Request for Sensitive Credentials / KYC" in categories:
        recommendations.append({
            "action": "Protect Your OTP & Banking Credentials",
            "priority": "Critical",
            "details": "Never disclose OTPs, PINs, CVVs, or NetBanking passwords. Banks and government bodies never request OTPs via SMS or chat."
        })

    # Fake Job / Task Scam
    if "Suspicious / Fake Job Offer Indicators" in categories:
        recommendations.append({
            "action": "Verify Corporate Recruitment Standards",
            "priority": "High",
            "details": "Legitimate employers never communicate hiring offers solely via Telegram/WhatsApp, nor do they require upfront 'registration fees' or ask you to like YouTube videos for pay."
        })

    # Shortened Links or APK Downloads
    if "Unverified or Shortened Links / Direct Redirect" in categories:
        recommendations.append({
            "action": "Do Not Open Links or Download APKs",
            "priority": "Critical",
            "details": "Scammers use shortened links to bypass security filters and prompt malicious APK installations that steal OTPs."
        })

    # Utility / Courier Scam
    if "Utility / Courier Delivery Scam Cues" in categories:
        recommendations.append({
            "action": "Check Official Utility / Courier Portal Directly",
            "priority": "High",
            "details": "Log in directly to your official electricity board portal or courier tracking site (e.g., India Post, Blue Dart). Do not pay via text message links."
        })

    # Financial / Lottery Lure
    if "Unrealistic Financial Rewards or Lottery" in categories:
        recommendations.append({
            "action": "Reject Unsolicited Prize Claims",
            "priority": "High",
            "details": "If you didn't enter a lottery, you cannot win one. Any 'prize' demanding an advance processing fee or tax payment is fraudulent."
        })

    # Default recommendation if low risk
    if not recommendations:
        recommendations.append({
            "action": "Maintain Everyday Vigilance",
            "priority": "Standard",
            "details": "This message exhibits normal communication patterns. However, always exercise caution if an unexpected request for money or personal data arises later."
        })

    return recommendations

def get_url_recommendations(url_analysis: dict) -> list:
    """
    Returns specific safety recommendations based on the URL inspection results.
    """
    recommendations = []
    risk_level = url_analysis.get("risk_level", "Low Risk")
    indicators = [ind["title"] for ind in url_analysis.get("indicators", [])]

    if risk_level in ["High Risk", "Moderate Risk"]:
        recommendations.append({
            "action": "Do Not Open or Enter Any Credentials",
            "priority": "Urgent",
            "details": "Do not visit this URL on your phone or computer. Never submit login credentials, card numbers, or passwords."
        })

    if any("Brand" in title for title in indicators):
        recommendations.append({
            "action": "Use the Official Bookmarked Website",
            "priority": "Critical",
            "details": "The analyzed URL is attempting to impersonate a reputable institution. Type the known official URL directly into your browser address bar."
        })

    if any("Shortened" in title for title in indicators):
        recommendations.append({
            "action": "Expand Shortened URLs Before Accessing",
            "priority": "High",
            "details": "Use a URL expander tool or verify the true destination before trusting a compressed bit.ly or tinyurl link."
        })

    if any("Insecure Protocol" in title for title in indicators):
        recommendations.append({
            "action": "Avoid Entering Data on Unencrypted Sites",
            "priority": "Medium",
            "details": "HTTP connections transmit your data in plaintext. Never conduct banking or enter passwords on non-HTTPS websites."
        })

    if not recommendations:
        recommendations.append({
            "action": "Standard Browsing Caution",
            "priority": "Standard",
            "details": "No blatant heuristic red flags were detected, but always verify the SSL padlock icon and domain spelling in your browser."
        })

    return recommendations

def get_emergency_protocol() -> dict:
    """
    Provides immediate incident response steps if a user has already fallen victim to a scam.
    """
    return {
        "helpline": {
            "name": "National Cyber Crime Helpline (India)",
            "phone": "1930",
            "portal": "https://cybercrime.gov.in",
            "description": "Available 24x7 to immediately report financial cyber fraud and freeze stolen funds in transit."
        },
        "immediate_actions": [
            {
                "step": "1. Freeze Compromised Bank Accounts / Cards",
                "instruction": "Call your bank's toll-free emergency fraud helpline immediately or use your mobile banking app to freeze net-banking and block cards."
            },
            {
                "step": "2. Disconnect & Isolate Infected Device",
                "instruction": "If you installed an APK or suspicious file, immediately turn off Wi-Fi and Mobile Data (or turn on Airplane Mode) to prevent remote access."
            },
            {
                "step": "3. Change Important Account Passwords",
                "instruction": "From a separate clean device, change passwords for your primary email, banking portals, and social media. Enable Multi-Factor Authentication (MFA)."
            },
            {
                "step": "4. Lodge an Official Police Complaint",
                "instruction": "Register an incident report at cybercrime.gov.in or visit your local Cyber Crime Police Station with screenshots, transaction IDs, and sender details."
            }
        ],
        "bank_contacts": BANK_EMERGENCY_CONTACTS
    }

def generate_incident_report(scan_type: str, raw_content: str, analysis: dict, recommendations: list) -> str:
    """
    Generates a structured forensic incident report that can be exported or downloaded
    for cybercrime filings (e.g. at 1930 or local police).
    """
    report_id = f"SCAMSHIELD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "=" * 65,
        "🛡️ SCAMSHIELD AI - FORENSIC INCIDENT INVESTIGATION REPORT",
        "=" * 65,
        f"Incident Reference ID : {report_id}",
        f"Report Generation Time: {timestamp}",
        f"Investigation Type    : {scan_type.upper()} THREAT ANALYSIS",
        f"Overall Threat Verdict: {analysis.get('verdict', 'N/A')}",
        f"Calculated Risk Score : {analysis.get('risk_score', 0)} / 100 ({analysis.get('risk_level', 'N/A')})",
        "=" * 65,
        "\n1. TARGET SUSPICIOUS CONTENT:",
        "-" * 30,
        raw_content.strip(),
        "\n2. FORENSIC INDICATORS & RED FLAGS DETECTED:",
        "-" * 45
    ]

    if scan_type == "Message":
        flags = analysis.get("red_flags", [])
        if flags:
            for i, f in enumerate(flags, 1):
                lines.append(f"  [{i}] {f['category']}")
                lines.append(f"      Details : {f['description']}")
                lines.append(f"      Evidence: {', '.join(f.get('matches', []))}")
        else:
            lines.append("  No overt linguistic social engineering indicators detected.")
        lines.append(f"\n  ML Probability Score: {analysis.get('ml_probability', 0)}%")
        lines.append(f"  Heuristic Flag Score: {analysis.get('heuristic_score', 0)}/100")
        lines.append(f"  Language Detected   : {analysis.get('language', 'English')}")
    else:
        indicators = analysis.get("indicators", [])
        if indicators:
            for i, ind in enumerate(indicators, 1):
                lines.append(f"  [{i}] [{ind['severity']}] {ind['title']}")
                lines.append(f"      Details: {ind['details']}")
        else:
            lines.append("  No structural heuristic anomalies identified.")
        lines.append(f"\n  Inspected Hostname: {analysis.get('hostname', 'N/A')}")
        lines.append(f"  Protocol Check    : {analysis.get('protocol', 'N/A')}")
        lines.append(f"  Entropy Level     : {analysis.get('entropy', 'N/A')}")

    lines.extend([
        "\n3. MANDATORY SAFETY & MITIGATION PROTOCOL:",
        "-" * 45
    ])
    for rec in recommendations:
        lines.append(f"  • [{rec['priority']} Priority] {rec['action']}")
        lines.append(f"    Instruction: {rec['details']}")

    lines.extend([
        "\n4. OFFICIAL EMERGENCY REPORTING (INDIA):",
        "-" * 45,
        "  • National Cyber Crime Helpline: 1930 (Toll-Free, 24x7)",
        "  • Official Reporting Portal    : https://cybercrime.gov.in",
        "  • In case of financial loss, contact your bank within the 1-hour 'Golden Period'.",
        "=" * 65,
        "DISCLAIMER: ScamShield AI provides heuristic decision assistance. This report is",
        "generated for informational security review and evidence compilation.",
        "=" * 65
    ])

    return "\n".join(lines)
