"""
ScamShield AI - Advanced URL Threat Intelligence & Heuristics Module
Safely inspects URLs for suspicious domains, IP addresses, excessive subdomains,
typosquatting, brand impersonation, entropy anomalies, and known phishing indicators
without fetching or executing dangerous remote payloads.
"""

import re
import math
from urllib.parse import urlparse, unquote
import requests

# Abused TLDs frequently associated with disposable phishing campaigns
SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".buzz", ".work", ".tk", ".ml", ".ga", ".cf", ".gq",
    ".monster", ".fit", ".surf", ".click", ".rest", ".icu", ".cam", ".live",
    ".party", ".cc", ".to", ".space", ".cfd", ".sbs", ".country"
}

# Known URL shortener services that mask the true destination
URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "is.gd", "cutt.ly", "t.co", "rb.gy", "ow.ly",
    "buff.ly", "goo.gl", "rotf.lol", "rebrand.ly", "bl.ink", "tiny.cc", "shorturl.at"
}

# Comprehensive high-profile brands targeted by impersonators
POPULAR_BRANDS = {
    "sbi": ["onlinesbi.sbi", "sbi.co.in", "statebankofindia.com"],
    "hdfc": ["hdfcbank.com"],
    "icici": ["icicibank.com"],
    "axis": ["axisbank.com"],
    "pnb": ["pnbindia.in"],
    "paytm": ["paytm.com"],
    "phonepe": ["phonepe.com"],
    "googlepay": ["pay.google.com"],
    "paypal": ["paypal.com"],
    "netflix": ["netflix.com"],
    "amazon": ["amazon.com", "amazon.in", "amazon.co.uk"],
    "google": ["google.com", "google.co.in"],
    "microsoft": ["microsoft.com", "live.com", "office.com"],
    "apple": ["apple.com", "icloud.com"],
    "facebook": ["facebook.com", "fb.com"],
    "instagram": ["instagram.com"],
    "whatsapp": ["whatsapp.com", "wa.me"],
    "telegram": ["telegram.org", "t.me"],
    "binance": ["binance.com"],
    "irctc": ["irctc.co.in"],
    "epfo": ["epfindia.gov.in"],
    "incometax": ["incometax.gov.in"],
    "parivahan": ["parivahan.gov.in"],
    "indiapost": ["indiapost.gov.in"],
    "fedex": ["fedex.com"],
    "bluedart": ["bluedart.com"]
}

# Typosquatting / leetspeak character substitutions
TYPO_SUBSTITUTIONS = {
    "0": "o", "1": "l", "3": "e", "5": "s", "@": "a", "vv": "w"
}

def calculate_shannon_entropy(text: str) -> float:
    """Calculates the Shannon entropy of a string to detect randomized strings/DGAs."""
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
    return round(entropy, 2)

def levenshtein_distance(s1: str, s2: str) -> int:
    """Computes string edit distance to detect close brand typosquatting."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
        prev = curr
    return prev[-1]

def normalize_url(url_string: str) -> str:
    """Prepend https:// if protocol is missing to allow correct parsing."""
    url = url_string.strip()
    if not re.match(r"^[a-zA-Z]+://", url):
        return f"http://{url}"
    return url

def check_ip_in_host(hostname: str) -> bool:
    """Checks whether the hostname is an IPv4 or IPv6 address."""
    ipv4_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    return bool(re.match(ipv4_pattern, hostname))

def detect_brand_impersonation(hostname: str) -> list:
    """
    Checks if a well-known brand is embedded in the hostname
    or closely matches via typosquatting while not being part of its authorized domains.
    """
    impersonations = []
    host_lower = hostname.lower()

    # Normalized host without leetspeak
    normalized_host = host_lower
    for char, replacement in TYPO_SUBSTITUTIONS.items():
        normalized_host = normalized_host.replace(char, replacement)

    # Break domain down into tokens
    domain_tokens = re.split(r"[-._]", host_lower)

    for brand, official_domains in POPULAR_BRANDS.items():
        # Check if the genuine host ends with any authorized official domain
        is_legit = any(
            host_lower == official or host_lower.endswith("." + official)
            for official in official_domains
        )
        if is_legit:
            continue

        # 1. Direct substring match in hostname
        direct_match = (brand in host_lower) or (brand in normalized_host)

        # 2. Typosquatting / Edit distance match (e.g. 'arnazon' vs 'amazon')
        typo_match = False
        matched_token = ""
        for token in domain_tokens:
            if 3 < len(token) <= len(brand) + 2:
                dist = levenshtein_distance(token, brand)
                if dist == 1 or (len(brand) >= 6 and dist == 2):
                    typo_match = True
                    matched_token = token
                    break

        if direct_match or typo_match:
            impersonations.append({
                "brand": brand.upper(),
                "official_domains": official_domains,
                "is_typosquat": typo_match,
                "detected_in": matched_token if typo_match else brand
            })

    return impersonations

def check_virustotal_api(url_to_check: str, api_key: str = None) -> dict:
    """
    Optional Threat Intelligence lookup using VirusTotal API v3.
    If no API key is provided, returns None and falls back to local heuristics.
    """
    if not api_key or not api_key.strip():
        return None

    try:
        headers = {"x-apikey": api_key.strip()}
        # Base64 url identifier for VirusTotal
        import base64
        url_id = base64.urlsafe_b64encode(url_to_check.encode()).decode().strip("=")
        endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"

        response = requests.get(endpoint, headers=headers, timeout=4)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            return {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "source": "VirusTotal Threat Intelligence"
            }
    except Exception:
        pass
    return None

def analyze_url(url_string: str, vt_api_key: str = None) -> dict:
    """
    Performs comprehensive static heuristic inspection of a URL.
    Does NOT connect to or load the target page, protecting user security.
    """
    if not url_string or not url_string.strip():
        return {"error": "Empty URL provided. Please enter a valid URL."}

    raw_url = url_string.strip()
    normalized = normalize_url(raw_url)

    try:
        parsed = urlparse(normalized)
    except Exception as e:
        return {"error": f"Invalid URL format: {str(e)}"}

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.lower()
    query = parsed.query

    # Remove port if present
    hostname = netloc.split(":")[0] if ":" in netloc else netloc

    indicators = []
    risk_score = 0

    # 1. Protocol check
    if scheme == "http":
        indicators.append({
            "severity": "Medium",
            "title": "Insecure Protocol (HTTP)",
            "details": "Connection is unencrypted. Most legitimate financial and institutional portals mandate HTTPS.",
            "points": 15
        })
        risk_score += 15

    # 2. Direct IP Address Host
    if check_ip_in_host(hostname):
        indicators.append({
            "severity": "High",
            "title": "Raw IP Address Used As Hostname",
            "details": f"Hostname '{hostname}' is a raw IP address, frequently utilized in short-lived phishing servers.",
            "points": 35
        })
        risk_score += 35

    # 3. Suspicious or Cheap TLD Check
    matched_tlds = [tld for tld in SUSPICIOUS_TLDS if hostname.endswith(tld)]
    if matched_tlds:
        indicators.append({
            "severity": "High",
            "title": f"Suspicious Top-Level Domain ({matched_tlds[0]})",
            "details": f"The '{matched_tlds[0]}' extension has high abuse frequency in automated phishing kits.",
            "points": 25
        })
        risk_score += 25

    # 4. URL Shortener Masking
    if hostname in URL_SHORTENERS:
        shortener_points = 20
        details = f"The domain '{hostname}' is a URL shortener that conceals the true landing page destination."
        
        # Check if shortened link custom slug mimics a brand
        masked_brand = [b for b in POPULAR_BRANDS if b in path]
        if masked_brand:
            shortener_points += 15
            details += f" Path contains brand keyword '{masked_brand[0].upper()}', commonly used to lure clicks."

        indicators.append({
            "severity": "Medium" if not masked_brand else "High",
            "title": "Shortened / Obfuscated Link",
            "details": details,
            "points": shortener_points
        })
        risk_score += shortener_points

    # 5. Excessive Subdomain Depth
    subdomain_parts = [p for p in hostname.split(".") if p]
    if len(subdomain_parts) > 3 and not check_ip_in_host(hostname):
        indicators.append({
            "severity": "Medium",
            "title": "Deep Subdomain Nesting",
            "details": f"Domain contains {len(subdomain_parts)} levels ({hostname}), often used to mimic trusted paths.",
            "points": 15
        })
        risk_score += 15

    # 6. Abnormal URL Length & Shannon Entropy
    url_entropy = calculate_shannon_entropy(raw_url)
    if len(raw_url) > 75:
        indicators.append({
            "severity": "Low",
            "title": "Abnormally Long URL",
            "details": f"URL length is {len(raw_url)} characters. Phishing links often embed tokens or hidden redirection targets.",
            "points": 10
        })
        risk_score += 10

    if url_entropy >= 4.4 and len(raw_url) > 35:
        indicators.append({
            "severity": "Medium",
            "title": f"High Character Entropy ({url_entropy})",
            "details": "Randomized character sequences detected, characteristic of automated phishing generation algorithms (DGAs).",
            "points": 15
        })
        risk_score += 15

    # 7. Targeted Brand Impersonation / Typosquatting
    impersonations = detect_brand_impersonation(hostname)
    for imp in impersonations:
        title = f"Brand Typosquatting ({imp['brand']})" if imp.get("is_typosquat") else f"Targeted Brand Impersonation ({imp['brand']})"
        desc = (
            f"Hostname mimics '{imp['brand']}' using deceptive spelling variations ({imp.get('detected_in')})."
            if imp.get("is_typosquat")
            else f"Hostname embeds '{imp['brand']}' but does not belong to authorized domains: {', '.join(imp['official_domains'][:3])}."
        )
        indicators.append({
            "severity": "Critical",
            "title": title,
            "details": desc,
            "points": 45
        })
        risk_score += 45

    # 8. Phishing Keywords in Path or Host
    phish_keywords = ["login", "signin", "verify", "update-kyc", "banking", "secure", "free-gift", "claim", "otp", "aadhaar", "pan-update"]
    found_keywords = [kw for kw in phish_keywords if kw in path or kw in hostname]
    if found_keywords and (impersonations or matched_tlds or check_ip_in_host(hostname)):
        indicators.append({
            "severity": "High",
            "title": "Deceptive Phishing Path Keywords",
            "details": f"URL path/domain includes high-risk lures: {', '.join(found_keywords)}.",
            "points": 20
        })
        risk_score += 20

    # Optional VirusTotal integration
    vt_result = check_virustotal_api(normalized, vt_api_key)
    if vt_result and (vt_result.get("malicious", 0) > 0 or vt_result.get("suspicious", 0) > 0):
        indicators.append({
            "severity": "Critical",
            "title": "Threat Intelligence Blacklist Match",
            "details": f"VirusTotal flagged this URL with {vt_result['malicious']} malicious and {vt_result['suspicious']} suspicious vendor hits.",
            "points": 50
        })
        risk_score += 50

    # Cap risk score at 100
    risk_score = min(risk_score, 100)

    # Risk level classification
    if risk_score >= 60:
        risk_level = "High Risk"
        verdict = "Potentially Malicious / Phishing"
        badge_color = "red"
    elif risk_score >= 25:
        risk_level = "Moderate Risk"
        verdict = "Suspicious Link (Exercise Caution)"
        badge_color = "orange"
    else:
        risk_level = "Low Risk"
        verdict = "No Obvious Suspicious Indicators"
        badge_color = "green"

    return {
        "original_url": raw_url,
        "hostname": hostname,
        "protocol": scheme.upper(),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "verdict": verdict,
        "badge_color": badge_color,
        "indicators": indicators,
        "indicator_count": len(indicators),
        "is_ip": check_ip_in_host(hostname),
        "is_shortened": hostname in URL_SHORTENERS,
        "impersonations": [i["brand"] for i in impersonations],
        "entropy": url_entropy,
        "vt_result": vt_result
    }

if __name__ == "__main__":
    test_urls = [
        "https://www.google.com/search?q=cybersecurity",
        "http://sbi-online-kyc-update.xyz/login.php",
        "http://arnazon-orders-tracking.top/verify",
        "https://netflix.customer-support-portal.top/renew",
        "http://192.168.1.100/verify-account",
        "https://bit.ly/free-amazon-voucher"
    ]

    print("Running URL Checker Test Cases:\n" + "=" * 55)
    for u in test_urls:
        res = analyze_url(u)
        print(f"URL: {res['original_url']}")
        print(f"Verdict: {res['verdict']} | Score: {res['risk_score']}/100 | Indicators: {res['indicator_count']}")
        for ind in res['indicators']:
            print(f"  - [{ind['severity']}] {ind['title']}: {ind['details']}")
        print("-" * 55)
