"""
ScamShield AI - Intelligent Digital Safety Assistant
Main Streamlit Application Dashboard
Tagline: Think Before You Click. Stay Safe Before You Trust.
"""

import streamlit as st
import pandas as pd
import io

from ml.predict import predict_message
from modules.url_checker import analyze_url
from modules.safety import (
    get_message_recommendations,
    get_url_recommendations,
    get_emergency_protocol,
    generate_incident_report
)
from modules.database import (
    init_db,
    add_scan_record,
    get_recent_scans,
    clear_history,
    get_scan_statistics,
    export_history_as_csv
)

# ---------------------------------------------------------
# Page Configuration & UI Theme Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="ScamShield AI | Digital Safety Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cybersecurity Dark UI with Glassmorphism
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }
    
    /* Top Banner Header */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
        border: 1px solid #38bdf840;
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.1);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-tagline {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 500;
    }

    /* Metric Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 18px;
        color: #f8fafc;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #38bdf880;
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 2.0rem;
        font-weight: 800;
        color: #38bdf8;
        margin-top: 4px;
    }

    /* Risk Badges */
    .badge-high {
        background-color: #ef444425;
        color: #f87171;
        border: 1px solid #ef4444;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
        letter-spacing: 0.03em;
    }
    .badge-medium {
        background-color: #f59e0b25;
        color: #fbbf24;
        border: 1px solid #f59e0b;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
        letter-spacing: 0.03em;
    }
    .badge-low {
        background-color: #10b98125;
        color: #34d399;
        border: 1px solid #10b981;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
        letter-spacing: 0.03em;
    }

    /* Red Flag Box */
    .flag-box {
        background-color: #450a0a25;
        border: 1px solid #991b1b60;
        border-left: 5px solid #ef4444;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    /* Safety Recommendation Box */
    .rec-box {
        background-color: #064e3b25;
        border: 1px solid #065f4660;
        border-left: 5px solid #10b981;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    /* Info Tip Box */
    .tip-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-left: 4px solid #38bdf8;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize local SQLite storage
init_db()

# ---------------------------------------------------------
# Sidebar Navigation & Settings
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("ScamShield AI")
    st.caption("🛡️ *Think Before You Click. Stay Safe Before You Trust.*")
    st.markdown("---")

    menu_option = st.radio(
        "Navigation Menu",
        [
            "🏠 Overview & Dashboard",
            "💬 Message & Job Scanner",
            "🔗 Suspicious URL Inspector",
            "🚨 Cyber Safety & Helplines",
            "🧠 Spot-the-Phish Quiz",
            "📜 Scan History & Logs"
        ],
        index=0
    )

    st.markdown("---")
    with st.expander("⚙️ Threat Intelligence Settings"):
        vt_api_key = st.text_input(
            "VirusTotal API Key (Optional):",
            type="password",
            help="Provide your VirusTotal API key for live external threat-intelligence lookups. If left blank, ScamShield runs autonomously on local heuristic threat engine."
        )
        if vt_api_key:
            st.success("VirusTotal API configured.")
        else:
            st.caption("Mode: 🛡️ **Autonomous Local Heuristic Engine** (Privacy-Preserving)")

    st.markdown("---")
    st.info(
        "**Hackathon Tech Stack:**\n\n"
        "• **Model:** TF-IDF + Logistic Regression (98.21% test accuracy)\n"
        "• **Explainability:** Regex linguistic heuristics (English + Hinglish)\n"
        "• **URL Engine:** Brand typosquatting & Shannon entropy analysis\n"
        "• **Storage:** Local SQLite database"
    )

# ---------------------------------------------------------
# Page 1: Overview & Central Hub
# ---------------------------------------------------------
if menu_option == "🏠 Overview & Dashboard":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🛡️ ScamShield AI - Central Security Hub</div>
        <div class="hero-tagline">Think Before You Click. Stay Safe Before You Trust.</div>
        <p style="margin-top: 10px; color: #cbd5e1; max-width: 850px;">
            An intelligent, privacy-preserving defense system engineered to detect SMS phishing (smishing),
            fraudulent WhatsApp employment offers, fake utility disconnection threats, and brand-spoofed URLs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    stats = get_scan_statistics()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Analyses</div>
            <div class="metric-value">{stats['total_scans']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">High Risk Intercepts</div>
            <div class="metric-value" style="color: #ef4444;">{stats['high_risk']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Suspicious Alerts</div>
            <div class="metric-value" style="color: #f59e0b;">{stats['moderate_risk']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Safe Verifications</div>
            <div class="metric-value" style="color: #10b981;">{stats['low_risk']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.subheader("⚡ Core Defense Capabilities")
        st.markdown("""
        - **🤖 Hybrid AI Architecture:** Combines TF-IDF Logistic Regression with real-time heuristic rule extraction to detect modern threats that static datasets miss.
        - **🌐 Multilingual & Hinglish Support:** Specially designed for Indian cybercrime vectors (*'Bijli cut ho jayega'*, *'Ghar baithe kamayein'*, *'Aadhaar KYC block'*).
        - **🔍 Safe URL Deconstruction:** Evaluates protocol, IP hosts, brand typosquatting (e.g. `arnazon.top`), and Shannon entropy without sending network pings.
        - **💡 Explainable AI (XAI):** Clear breakdown of *why* an input is dangerous, highlighting specific keywords and social engineering tactics.
        - **📄 Forensic Report Generation:** Instant exportable incident reports ready to present at police stations or on `cybercrime.gov.in`.
        """)

        st.subheader("⚠️ Top 4 Modern Social Engineering Traps")
        tab1, tab2, tab3, tab4 = st.tabs(["Part-Time Task Scam", "Electricity Bill Panic", "Digital Arrest", "Courier Delivery"])
        with tab1:
            st.markdown("""
            > **Tactic:** *"Earn ₹3,000 - ₹8,000 daily by liking YouTube videos. Work from home. Contact HR on WhatsApp/Telegram."*  
            > **The Trap:** Starts with ₹150 payouts to earn trust, then coerces victims to deposit money into bogus crypto/VIP tasks.
            """)
        with tab2:
            st.markdown("""
            > **Tactic:** *"Dear consumer, your power will be disconnected at 9:30 PM due to unpaid bill. Update KYC immediately or call officer..."*  
            > **The Trap:** Induces panic and forces downloading malicious remote-access APKs.
            """)
        with tab3:
            st.markdown("""
            > **Tactic:** *"CBI Officer speaking: A parcel in your name contains narcotics. You are under Digital Arrest. Join Skype call now."*  
            > **The Trap:** Fake police uniforms on video calls coercing victims to transfer life savings for 'verification'.
            """)
        with tab4:
            st.markdown("""
            > **Tactic:** *"India Post: Your package failed delivery due to missing address. Pay ₹25 re-delivery fee at bit.ly/..."*  
            > **The Trap:** Clones official courier portals to harvest debit/credit card numbers and OTPs.
            """)

    with col_right:
        st.subheader("🚀 Quick Evaluation Console")
        quick_type = st.radio("Choose Input Type:", ["Message / Job Offer", "Suspicious URL"], horizontal=True)

        if quick_type == "Message / Job Offer":
            sample_choice = st.selectbox(
                "Or load a preset sample:",
                [
                    "-- Select or type custom below --",
                    "Electricity Bill Disconnection Scam (English)",
                    "Bijli Cut Scam (Hinglish)",
                    "Fake Part-Time YouTube Job Offer",
                    "Digital Arrest Extortion Threat",
                    "Bank Account KYC Expiry Phishing",
                    "Legitimate Meeting Confirmation"
                ]
            )

            presets = {
                "Electricity Bill Disconnection Scam (English)": "Dear consumer your electricity power will be disconnected tonight at 9:30 PM because your previous month bill was not updated. Please immediately contact our electricity officer at 9876543210 or update KYC at bit.ly/power-bill",
                "Bijli Cut Scam (Hinglish)": "Aapka bijli connection aaj raat 9:30 baje disconnect ho jayega. Turant apna bill bharein aur KYC update karein: bit.ly/bijli-pay",
                "Fake Part-Time YouTube Job Offer": "Amazon HR Recruitment: Earn ₹2500 - ₹5000 daily by simply rating products and liking YouTube videos. Work 1 hour from home. Contact HR now on WhatsApp: wa.me/919999988888",
                "Digital Arrest Extortion Threat": "Digital Arrest Warning: CBI officer speaking. Your parcel containing illegal narcotics seized at customs. Join Skype call immediately or face arrest warrant.",
                "Bank Account KYC Expiry Phishing": "Your SBI Bank account is suspended today due to pending KYC verification. Please click here to submit your Aadhaar and update PAN: http://sbi-online-kyc-portal.xyz/login.php",
                "Legitimate Meeting Confirmation": "Hi team, please find attached the presentation slides for tomorrow's project review at 10 AM. Let me know if any updates are needed."
            }

            default_text = presets.get(sample_choice, "")
            user_input_msg = st.text_area("Message Text:", value=default_text, height=120, placeholder="Paste text here...")

            if st.button("🚀 Analyze Message Now", use_container_width=True, type="primary"):
                if user_input_msg.strip():
                    res = predict_message(user_input_msg)
                    add_scan_record("Message", user_input_msg, res["risk_score"], res["risk_level"], res["verdict"], res["flag_count"])
                    st.success(f"Result: **{res['verdict']}** (Risk Score: {res['risk_score']}%)")
                    st.info("Switch to the **'Message & Job Scanner'** in the sidebar for full explainability and report export!")
                else:
                    st.warning("Please enter some text first.")

        else:
            url_sample = st.selectbox(
                "Or load a preset URL:",
                [
                    "-- Select or type custom below --",
                    "http://sbi-online-kyc-update.xyz/login.php",
                    "http://arnazon-orders-tracking.top/verify",
                    "https://netflix.customer-support-portal.top/renew",
                    "http://192.168.1.100/verify-account",
                    "https://bit.ly/free-amazon-voucher",
                    "https://www.google.com/search?q=cybersecurity"
                ]
            )
            default_url = "" if url_sample.startswith("--") else url_sample
            user_url = st.text_input("Website URL:", value=default_url, placeholder="e.g. sbi-kyc-update.xyz")

            if st.button("🔎 Inspect URL Now", use_container_width=True, type="primary"):
                if user_url.strip():
                    u_res = analyze_url(user_url, vt_api_key)
                    add_scan_record("URL", user_url, u_res["risk_score"], u_res["risk_level"], u_res["verdict"], u_res["indicator_count"])
                    st.success(f"Result: **{u_res['verdict']}** (Risk Score: {u_res['risk_score']}/100)")
                    st.info("Switch to the **'Suspicious URL Inspector'** in the sidebar for deep threat breakdown!")
                else:
                    st.warning("Please enter a URL first.")

# ---------------------------------------------------------
# Page 2: Message & Job Scanner
# ---------------------------------------------------------
elif menu_option == "💬 Message & Job Scanner":
    st.title("💬 Message & Job Offer Scam Detector")
    st.markdown(
        "Scan incoming SMS alerts, WhatsApp forwards, suspicious internship/job offers, "
        "and payment requests for social engineering and fraudulent patterns."
    )

    # Sample Buttons for 1-click evaluation
    st.markdown("**💡 1-Click Evaluation Presets:**")
    p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns(5)

    if "loaded_msg" not in st.session_state:
        st.session_state.loaded_msg = ""

    with p_col1:
        if st.button("⚡ Electricity Scam"):
            st.session_state.loaded_msg = "URGENT: Your electricity connection will be disconnected tonight at 9:30 PM due to unpaid bill. Call officer immediately at 9876543210 or update KYC at bit.ly/elec-pay"
    with p_col2:
        if st.button("🇮🇳 Bijli Scam (Hinglish)"):
            st.session_state.loaded_msg = "Aapka bijli connection aaj raat 9:30 baje disconnect ho jayega. Turant apna bill bharein aur KYC update karein: bit.ly/bijli-pay"
    with p_col3:
        if st.button("💼 Fake Job Offer"):
            st.session_state.loaded_msg = "Part-Time Work from Home Opportunity! Earn ₹3000 to ₹7000 daily by liking YouTube videos and rating hotels. No experience needed. Contact HR manager on Telegram @JobHR_Manager"
    with p_col4:
        if st.button("🚨 Digital Arrest"):
            st.session_state.loaded_msg = "Digital Arrest Notice: CBI officer speaking. Your courier parcel containing narcotics seized. Skype call immediately or face non-bailable arrest warrant."
    with p_col5:
        if st.button("✅ Legitimate SMS"):
            st.session_state.loaded_msg = "Hey Rahul, don't forget our team sync tomorrow at 10 AM in the main conference room. See you there!"

    input_text = st.text_area(
        "Enter or paste the message text below:",
        value=st.session_state.loaded_msg,
        height=140,
        placeholder="Paste suspicious SMS, WhatsApp message, or job offer here..."
    )

    col_btn, col_batch, col_clear = st.columns([1.5, 2, 1])
    with col_btn:
        analyze_btn = st.button("🛡️ Analyze Message", type="primary", use_container_width=True)
    with col_clear:
        if st.button("🧹 Clear Input", use_container_width=True):
            st.session_state.loaded_msg = ""
            st.rerun()

    # Batch File Upload Option
    with st.expander("📁 Batch File Scan (.TXT or .CSV)"):
        uploaded_file = st.file_uploader("Upload message list (one message per line or CSV):", type=["txt", "csv"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df_up = pd.read_csv(uploaded_file)
                    col_to_scan = df_up.columns[0]
                    lines = df_up[col_to_scan].dropna().astype(str).tolist()[:25]
                else:
                    lines = [line.decode("utf-8", errors="ignore").strip() for line in uploaded_file if line.strip()][:25]

                st.write(f"Loaded **{len(lines)} messages** for batch scanning:")
                if st.button("Run Batch Analysis"):
                    batch_results = []
                    for item in lines:
                        r = predict_message(item)
                        batch_results.append({
                            "Message": item[:60] + "...",
                            "Risk Score (%)": r["risk_score"],
                            "Risk Level": r["risk_level"],
                            "Verdict": r["verdict"],
                            "Language": r["language"]
                        })
                    st.dataframe(pd.DataFrame(batch_results), use_container_width=True)
            except Exception as e:
                st.error(f"Error parsing batch file: {e}")

    if analyze_btn:
        if not input_text.strip():
            st.warning("⚠️ Please provide a message to analyze.")
        else:
            with st.spinner("Analyzing message text through ScamShield AI..."):
                result = predict_message(input_text)
                recs = get_message_recommendations(result)

                # Save record to database
                add_scan_record(
                    "Message",
                    input_text,
                    result["risk_score"],
                    result["risk_level"],
                    result["verdict"],
                    result["flag_count"]
                )

            st.markdown("---")
            st.subheader("📊 Analysis Verdict & Threat Rating")

            res_col1, res_col2, res_col3, res_col4 = st.columns([1.2, 1, 1, 1])

            with res_col1:
                badge_class = "badge-high" if result["risk_level"] == "High Risk" else ("badge-medium" if result["risk_level"] == "Moderate Risk" else "badge-low")
                st.markdown(f"**Threat Assessment:**")
                st.markdown(f"<div class='{badge_class}' style='font-size: 1.1rem;'>{result['verdict']}</div>", unsafe_allow_html=True)
                st.caption(f"Risk Tier: **{result['risk_level']}**")

            with res_col2:
                st.metric("Composite Risk Score", f"{result['risk_score']}%")
                st.progress(result["risk_score"] / 100.0)

            with res_col3:
                st.metric("ML Model Probability", f"{result['ml_probability']}%")
                st.caption(f"Heuristic Flag Match: {result['heuristic_score']}/100")

            with res_col4:
                st.metric("Language Detected", result["language"])
                st.caption(f"Flags Found: {result['flag_count']}")

            # Explainable Red Flags Section
            st.markdown("---")
            st.subheader(f"🔍 Explainable Warning Signs ({result['flag_count']} Detected)")

            if result["red_flags"]:
                for flag in result["red_flags"]:
                    st.markdown(f"""
                    <div class="flag-box">
                        <strong style="color: #ef4444; font-size: 1.05rem;">🚨 {flag['category']}</strong> 
                        <span style="color: #94a3b8; font-size: 0.9rem;">({flag['category_hi']})</span><br/>
                        <span style="color: #e2e8f0;">{flag['description']}</span><br/>
                        <span style="color: #94a3b8; font-size: 0.9rem;">Triggered by matches: <code>{', '.join(flag['matches'])}</code></span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ **No obvious linguistic scam indicators found.** Message structure appears typical.")

            # Safety Recommendations Section
            st.markdown("---")
            st.subheader("💡 Recommended Safety Actions")
            for rec in recs:
                st.markdown(f"""
                <div class="rec-box">
                    <strong style="color: #10b981; font-size: 1.05rem;">👉 {rec['action']} [{rec['priority']} Priority]</strong><br/>
                    <span style="color: #cbd5e1;">{rec['details']}</span>
                </div>
                """, unsafe_allow_html=True)

            # Forensic Incident Report Download
            st.markdown("---")
            st.subheader("📄 Export Forensic Incident Report")
            st.caption("Generate a structured investigation summary suitable for filing official complaints at 1930 / cybercrime.gov.in.")
            report_text = generate_incident_report("Message", input_text, result, recs)

            st.download_button(
                label="📥 Download Forensic Report (.txt)",
                data=report_text,
                file_name=f"scamshield_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ---------------------------------------------------------
# Page 3: Suspicious URL Inspector
# ---------------------------------------------------------
elif menu_option == "🔗 Suspicious URL Inspector":
    st.title("🔗 Suspicious URL & Domain Inspector")
    st.markdown(
        "Inspect hyperlinks, phishing domains, and shortened links without ever opening them. "
        "ScamShield uses static heuristic security analysis to inspect structural attributes, brand typosquatting, and Shannon entropy."
    )

    st.markdown("**💡 1-Click Evaluation Presets:**")
    u_col1, u_col2, u_col3, u_col4, u_col5 = st.columns(5)

    if "loaded_url" not in st.session_state:
        st.session_state.loaded_url = ""

    with u_col1:
        if st.button("🏦 Spoofed SBI Bank"):
            st.session_state.loaded_url = "http://sbi-online-kyc-update.xyz/login.php"
    with u_col2:
        if st.button("🛍️ Amazon Typosquat"):
            st.session_state.loaded_url = "http://arnazon-orders-tracking.top/verify"
    with u_col3:
        if st.button("🎬 Fake Netflix Portal"):
            st.session_state.loaded_url = "https://netflix.customer-support-portal.top/renew"
    with u_col4:
        if st.button("🌐 Raw IP Address"):
            st.session_state.loaded_url = "http://192.168.1.100/verify-account"
    with u_col5:
        if st.button("✅ Official Safe Site"):
            st.session_state.loaded_url = "https://www.google.com/search?q=cybersecurity"

    url_input = st.text_input(
        "Enter target URL or domain to inspect:",
        value=st.session_state.loaded_url,
        placeholder="e.g. http://sbi-online-kyc.xyz/update"
    )

    if st.button("🔍 Inspect URL Safely", type="primary"):
        if not url_input.strip():
            st.warning("⚠️ Please provide a URL to inspect.")
        else:
            with st.spinner("Deconstructing URL and checking threat indicators..."):
                u_res = analyze_url(url_input, vt_api_key)
                u_recs = get_url_recommendations(u_res)

                # Save record to database
                add_scan_record(
                    "URL",
                    url_input,
                    u_res["risk_score"],
                    u_res["risk_level"],
                    u_res["verdict"],
                    u_res["indicator_count"]
                )

            st.markdown("---")
            st.subheader("📊 URL Risk Verdict")

            col_u1, col_u2, col_u3, col_u4 = st.columns([1.2, 1, 1.2, 1])

            with col_u1:
                badge_class = "badge-high" if u_res["risk_level"] == "High Risk" else ("badge-medium" if u_res["risk_level"] == "Moderate Risk" else "badge-low")
                st.markdown("**Verdict:**")
                st.markdown(f"<div class='{badge_class}' style='font-size: 1.1rem;'>{u_res['verdict']}</div>", unsafe_allow_html=True)
                st.caption(f"Risk Tier: **{u_res['risk_level']}**")

            with col_u2:
                st.metric("Threat Score", f"{u_res['risk_score']} / 100")
                st.progress(u_res["risk_score"] / 100.0)

            with col_u3:
                st.markdown("**URL Structural Breakdown:**")
                st.caption(f"• **Protocol:** `{u_res['protocol']}`")
                st.caption(f"• **Hostname:** `{u_res['hostname']}`")
                st.caption(f"• **Raw IP Address:** `{'Yes ⚠️' if u_res['is_ip'] else 'No'}`")
                st.caption(f"• **Shortened Link:** `{'Yes ⚠️' if u_res['is_shortened'] else 'No'}`")

            with col_u4:
                st.metric("Entropy Level", f"{u_res['entropy']}")
                st.caption("Values > 4.2 indicate high randomness / DGA")

            # Threat Indicators Details
            st.markdown("---")
            st.subheader(f"⚠️ Structural Warning Indicators ({u_res['indicator_count']} Found)")

            if u_res["indicators"]:
                for ind in u_res["indicators"]:
                    st.markdown(f"""
                    <div class="flag-box">
                        <strong style="color: #ef4444; font-size: 1.05rem;">[{ind['severity']}] {ind['title']}</strong><br/>
                        <span style="color: #e2e8f0;">{ind['details']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ **No obvious heuristic anomalies detected.** Standard domain structure observed.")

            # Safety Recommendations Section
            st.markdown("---")
            st.subheader("💡 Safety Guidelines For This Link")
            for rec in u_recs:
                st.markdown(f"""
                <div class="rec-box">
                    <strong style="color: #10b981; font-size: 1.05rem;">👉 {rec['action']} [{rec['priority']} Priority]</strong><br/>
                    <span style="color: #cbd5e1;">{rec['details']}</span>
                </div>
                """, unsafe_allow_html=True)

            # Forensic Incident Report Download
            st.markdown("---")
            st.subheader("📄 Export Forensic URL Report")
            u_report_text = generate_incident_report("URL", url_input, u_res, u_recs)

            st.download_button(
                label="📥 Download URL Threat Report (.txt)",
                data=u_report_text,
                file_name=f"scamshield_url_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.caption("🛡️ *Privacy Guarantee: This tool parses and inspects URL syntax locally. It never pings, renders, or triggers remote scripts.*")

# ---------------------------------------------------------
# Page 4: Cyber Safety & Helplines
# ---------------------------------------------------------
elif menu_option == "🚨 Cyber Safety & Helplines":
    st.title("🚨 Cyber Safety Awareness & Incident Response")
    st.markdown(
        "Practical security protocols and emergency response resources to safeguard yourself and your family."
    )

    emergency = get_emergency_protocol()

    st.error(f"""
    ### 🆘 Immediate Cyber Emergency Hotline (India)
    - **Helpline Number:** Dial **`{emergency['helpline']['phone']}`** (Toll-Free, 24x7)
    - **Official Portal:** [{emergency['helpline']['portal']}]({emergency['helpline']['portal']})
    - **Purpose:** {emergency['helpline']['description']}
    """)

    st.subheader("⚡ The 'Golden Hour' Response Protocol")
    st.markdown("If you accidentally shared OTPs, transferred money, or clicked a malicious link, follow these 4 steps immediately:")

    for action in emergency["immediate_actions"]:
        st.markdown(f"""
        <div class="rec-box">
            <strong style="color: #38bdf8; font-size: 1.05rem;">{action['step']}</strong><br/>
            <span style="color: #e2e8f0;">{action['instruction']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🏦 Major Banks Emergency Fraud Helplines")
    b_col1, b_col2, b_col3 = st.columns(3)
    banks = list(emergency["bank_contacts"].items())

    with b_col1:
        for b_name, b_info in banks[:2]:
            st.markdown(f"""
            <div class="tip-box">
                <strong style="color: #38bdf8;">{b_name}</strong><br/>
                <span>📞 Toll-Free: <code>{b_info['toll_free']}</code></span><br/>
                <span style="font-size: 0.85rem; color: #94a3b8;">{b_info['sms_block']}</span>
            </div>
            """, unsafe_allow_html=True)

    with b_col2:
        for b_name, b_info in banks[2:4]:
            st.markdown(f"""
            <div class="tip-box">
                <strong style="color: #38bdf8;">{b_name}</strong><br/>
                <span>📞 Toll-Free: <code>{b_info['toll_free']}</code></span><br/>
                <span style="font-size: 0.85rem; color: #94a3b8;">{b_info['sms_block']}</span>
            </div>
            """, unsafe_allow_html=True)

    with b_col3:
        for b_name, b_info in banks[4:]:
            st.markdown(f"""
            <div class="tip-box">
                <strong style="color: #38bdf8;">{b_name}</strong><br/>
                <span>📞 Toll-Free: <code>{b_info['toll_free']}</code></span><br/>
                <span style="font-size: 0.85rem; color: #94a3b8;">{b_info['sms_block']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🇮🇳 हिंदी में जन-जागरूकता (Hindi Awareness Tip)")
    st.info(
        "**सावधान रहें:** बैंक, बिजली विभाग या कोई भी सरकारी संस्था कभी भी फोन या मैसेज पर OTP, पासवर्ड या एटीएम पिन नहीं मांगती। "
        "किसी भी अनजान लिंक पर क्लिक न करें। धोखाधड़ी की स्थिति में तुरंत **1930** पर कॉल करें।"
    )

# ---------------------------------------------------------
# Page 5: Spot-the-Phish Quiz (Interactive Innovation)
# ---------------------------------------------------------
elif menu_option == "🧠 Spot-the-Phish Quiz":
    st.title("🧠 Test Your Scam IQ: Spot the Phish")
    st.markdown("Challenge yourself or demonstrate your security awareness to hackathon judges with this interactive mini-quiz!")

    q1 = st.radio(
        "**Question 1:** You receive an SMS: *'Your power will be cut in 2 hours unless you call 9876543210 to update KYC.'* What should you do?",
        [
            "Call the number immediately to avoid power loss.",
            "Click any attached link to settle the bill fast.",
            "Do NOT call the number. Check your electricity bill independently and verify on the official board website.",
            "Forward the message to your neighbors to warn them."
        ],
        index=None
    )
    if q1:
        if q1.startswith("Do NOT call"):
            st.success("✅ **Correct!** Electricity boards never disconnect power within 2 hours via SMS. Always verify via official bills.")
        else:
            st.error("❌ **Incorrect.** This is a classic urgency scam! Scammers create fear to make you call an unauthorized extortionist.")

    st.markdown("---")
    q2 = st.radio(
        "**Question 2:** An HR manager on Telegram asks you to like 5 YouTube videos to earn ₹500, but later requires a ₹1,000 'security deposit' for VIP tasks. Is this genuine?",
        [
            "Yes, many multinational tech companies recruit this way.",
            "No, this is a textbook Task / Investment Scam. Legitimate employers never charge advance security deposits.",
            "Yes, as long as they provide an ID card over Telegram.",
            "Maybe, if the company name is Amazon or Google."
        ],
        index=None
    )
    if q2:
        if q2.startswith("No, this is a textbook"):
            st.success("✅ **Correct!** Legitimate organizations never hire solely via Telegram or demand fees for work.")
        else:
            st.error("❌ **Incorrect.** No legitimate company asks employees to deposit money to unlock tasks!")

    st.markdown("---")
    q3 = st.radio(
        "**Question 3:** Which of the following URLs is an official State Bank of India portal?",
        [
            "http://sbi-online-kyc-update.xyz/login.php",
            "https://onlinesbi.sbi",
            "http://statebank-secure-banking.top/login",
            "https://sbi.customer-support-portal.club/auth"
        ],
        index=None
    )
    if q3:
        if q3 == "https://onlinesbi.sbi":
            st.success("✅ **Correct!** SBI's authorized banking portal is `onlinesbi.sbi`. The other links use disposable `.xyz`, `.top`, and `.club` TLDs to impersonate the bank.")
        else:
            st.error("❌ **Incorrect.** That is an impersonation phishing domain! SBI owns the authorized top-level domain `.sbi`.")

# ---------------------------------------------------------
# Page 6: Scan History & Logs
# ---------------------------------------------------------
elif menu_option == "📜 Scan History & Logs":
    st.title("📜 Scan History & Analytics")
    st.markdown("Review recent analyses conducted in this session. All records are stored locally in your SQLite database.")

    scans = get_recent_scans(limit=100)

    if not scans:
        st.info("No scan records found yet. Use the Message Scanner or URL Inspector to analyze threats!")
    else:
        df_history = pd.DataFrame(scans)
        
        # Summary metrics
        total = len(df_history)
        high = (df_history["risk_level"] == "High Risk").sum()
        mod = (df_history["risk_level"] == "Moderate Risk").sum()
        low = (df_history["risk_level"] == "Low Risk").sum()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Scans Logged", total)
        m2.metric("High Risk", int(high))
        m3.metric("Moderate Risk", int(mod))
        m4.metric("Low Risk", int(low))

        st.markdown("---")
        st.subheader("Recent Scan Records")

        # Format dataframe for display
        display_df = df_history[["timestamp", "scan_type", "content_snippet", "risk_score", "risk_level", "verdict", "flags_count"]].copy()
        display_df.columns = ["Timestamp", "Type", "Content Snippet", "Risk Score (%)", "Risk Level", "Verdict", "Flags Detected"]

        st.dataframe(display_df, use_container_width=True)

        col_csv, col_del = st.columns([1, 1])
        with col_csv:
            csv_data = export_history_as_csv()
            st.download_button(
                label="📥 Export History as CSV",
                data=csv_data,
                file_name=f"scamshield_history_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_del:
            if st.button("🗑️ Clear All Scan History", type="secondary", use_container_width=True):
                clear_history()
                st.success("Scan history cleared successfully!")
                st.rerun()

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.85rem; padding-bottom: 20px;'>"
    "🛡️ <b>ScamShield AI</b> • Enterprise Digital Safety Assistant • Think Before You Click. Stay Safe Before You Trust."
    "</div>",
    unsafe_allow_html=True
)
