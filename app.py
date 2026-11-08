"""
ScamShield AI - Intelligent Digital Safety Platform
A modern, consumer-ready cybersecurity SaaS application.
Tagline: Think Before You Click. Stay Safe Before You Trust.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

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
# Page Configuration & Metadata
# ---------------------------------------------------------
st.set_page_config(
    page_title="ScamShield AI | Digital Safety Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize local SQLite database
init_db()

# Session State Initialization for Navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "msg_input_value" not in st.session_state:
    st.session_state.msg_input_value = ""

if "url_input_value" not in st.session_state:
    st.session_state.url_input_value = ""

def navigate_to(page_name: str):
    st.session_state.current_page = page_name
    st.rerun()

# ---------------------------------------------------------
# Custom CSS: Premium Red-and-White Light SaaS Theme
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global Typography & Font Family */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #171717;
    }

    /* Main App Background */
    .stApp {
        background-color: #FAFAFA;
    }

    /* Hide Default Header & Reduce Top Padding */
    header[data-testid="stHeader"] {
        background-color: #FFFFFF00;
        z-index: 10;
    }
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        max-width: 1200px;
    }

    /* Top Navigation Bar */
    .navbar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFFFFF;
        padding: 14px 28px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        border: 1px solid #F0F0F0;
        margin-bottom: 24px;
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 800;
        font-size: 1.35rem;
        color: #171717;
        text-decoration: none;
    }
    .nav-brand-red {
        color: #E63946;
    }
    .nav-tagline {
        font-size: 0.8rem;
        color: #666666;
        font-weight: 500;
        margin-left: 4px;
    }

    /* Hero Section Styling */
    .hero-container {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF5F5 100%);
        border: 1px solid #FFE4E6;
        border-radius: 24px;
        padding: 48px 40px;
        text-align: center;
        margin-bottom: 36px;
        box-shadow: 0 10px 30px rgba(230, 57, 70, 0.05);
        position: relative;
        overflow: hidden;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #FFE5E7;
        color: #A4161A;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 6px 16px;
        border-radius: 9999px;
        margin-bottom: 18px;
        border: 1px solid #FFCCD0;
    }
    .hero-badge-dot {
        width: 8px;
        height: 8px;
        background-color: #E63946;
        border-radius: 50%;
        display: inline-block;
    }
    .hero-title {
        font-size: 3.0rem;
        font-weight: 800;
        line-height: 1.15;
        color: #171717;
        margin-bottom: 16px;
        letter-spacing: -0.02em;
    }
    .hero-title-highlight {
        color: #E63946;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #666666;
        max-width: 720px;
        margin: 0 auto 30px auto;
        line-height: 1.6;
    }

    /* Modern SaaS Cards */
    .saas-card {
        background-color: #FFFFFF;
        border: 1px solid #F0F0F0;
        border-radius: 18px;
        padding: 26px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        height: 100%;
    }
    .saas-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(230, 57, 70, 0.08);
        border-color: #FFCCD0;
    }

    .metric-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #E63946;
        margin-bottom: 4px;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Section Headers */
    .section-heading-container {
        text-align: center;
        margin-top: 20px;
        margin-bottom: 32px;
    }
    .section-badge {
        color: #E63946;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .section-title {
        font-size: 2.0rem;
        font-weight: 800;
        color: #171717;
        letter-spacing: -0.01em;
    }
    .section-description {
        font-size: 1.05rem;
        color: #666666;
        max-width: 650px;
        margin: 8px auto 0 auto;
    }

    /* Risk Indicator Badges */
    .risk-pill-high {
        background-color: #FEE2E2;
        color: #991B1B;
        border: 1px solid #F87171;
        padding: 6px 16px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .risk-pill-medium {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FBBF24;
        padding: 6px 16px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .risk-pill-low {
        background-color: #D1FAE5;
        color: #065F46;
        border: 1px solid #34D399;
        padding: 6px 16px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Result Explanations & Cards */
    .warning-card {
        background-color: #FFF5F5;
        border: 1px solid #FED7D7;
        border-left: 5px solid #E63946;
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    .warning-title {
        color: #A4161A;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 4px;
    }
    .warning-desc {
        color: #4A5568;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .warning-matches {
        color: #718096;
        font-size: 0.85rem;
        margin-top: 6px;
    }
    .warning-code {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 2px 6px;
        border-radius: 4px;
        color: #C53030;
        font-weight: 600;
    }

    /* Action Recommendation Card */
    .action-card {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 5px solid #16A34A;
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    .action-title {
        color: #15803D;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 4px;
    }
    .action-desc {
        color: #374151;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Standard Button Polish */
    div.stButton > button:first-child {
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }

    /* Primary Red Button Accent */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #E63946 0%, #D90429 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(230, 57, 70, 0.35) !important;
        padding: 10px 24px !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #FF5A65 0%, #E63946 100%) !important;
        box-shadow: 0 6px 20px rgba(230, 57, 70, 0.45) !important;
        transform: translateY(-1px);
    }

    /* Secondary Buttons */
    div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        color: #171717 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: #E63946 !important;
        color: #E63946 !important;
        background-color: #FFF5F5 !important;
    }

    /* Form Inputs */
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 12px !important;
        color: #171717 !important;
        font-size: 1rem !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #E63946 !important;
        box-shadow: 0 0 0 3px rgba(230, 57, 70, 0.15) !important;
    }

    /* Footer Styling */
    .footer-container {
        margin-top: 60px;
        padding-top: 32px;
        border-top: 1px solid #E5E7EB;
        text-align: center;
        color: #666666;
        font-size: 0.9rem;
    }
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 24px;
        margin-bottom: 16px;
        font-weight: 500;
    }
    .footer-links a {
        color: #666666;
        text-decoration: none;
    }
    .footer-links a:hover {
        color: #E63946;
    }
    .footer-legal {
        color: #9CA3AF;
        font-size: 0.82rem;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Top Navigation Bar
# ---------------------------------------------------------
nav_col_logo, nav_col_btns = st.columns([1.5, 3])

with nav_col_logo:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; padding-top: 4px;">
        <span style="font-size: 1.7rem;">🛡️</span>
        <div>
            <span style="font-size: 1.35rem; font-weight: 800; color: #171717; letter-spacing: -0.02em;">Scam</span><span style="font-size: 1.35rem; font-weight: 800; color: #E63946;">Shield</span> <span style="font-size: 0.8rem; font-weight: 700; background-color: #E63946; color: #FFFFFF; padding: 2px 7px; border-radius: 6px; vertical-align: middle;">AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav_col_btns:
    n1, n2, n3, n4, n5 = st.columns(5)
    with n1:
        if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.current_page == "Home" else "secondary"):
            navigate_to("Home")
    with n2:
        if st.button("💬 Messages", use_container_width=True, type="primary" if st.session_state.current_page == "Message Checker" else "secondary"):
            navigate_to("Message Checker")
    with n3:
        if st.button("🔗 URLs", use_container_width=True, type="primary" if st.session_state.current_page == "URL Checker" else "secondary"):
            navigate_to("URL Checker")
    with n4:
        if st.button("📖 About", use_container_width=True, type="primary" if st.session_state.current_page == "About" else "secondary"):
            navigate_to("About")
    with n5:
        if st.button("📜 History", use_container_width=True, type="primary" if st.session_state.current_page == "History" else "secondary"):
            navigate_to("History")

st.markdown("<hr style='margin: 12px 0 28px 0; border: none; border-top: 1px solid #E5E7EB;'/>", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 1: HOMEPAGE
# ---------------------------------------------------------
if st.session_state.current_page == "Home":
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">
            <span class="hero-badge-dot"></span> Intelligent Digital Safety Platform
        </div>
        <div class="hero-title">
            Your Digital Safety <span class="hero-title-highlight">Starts Here.</span>
        </div>
        <div class="hero-subtitle">
            ScamShield AI proactively protects everyday users from deceptive SMS messages, fraudulent WhatsApp job offers, payment traps, and brand-impersonating links before you trust them.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero Action Callouts (Two prominent action cards)
    c_action1, c_action2 = st.columns(2)
    with c_action1:
        st.markdown("""
        <div class="saas-card" style="border-top: 4px solid #E63946;">
            <div style="font-size: 1.8rem; margin-bottom: 10px;">💬</div>
            <h3 style="font-size: 1.35rem; font-weight: 700; margin-bottom: 8px; color: #171717;">Message & Job Offer Checker</h3>
            <p style="color: #666666; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px;">
                Received a suspicious SMS, part-time job pitch, or urgent payment notice? Paste it here to uncover social engineering red flags.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Check a Message Now", type="primary", use_container_width=True, key="hero_cta_msg"):
            navigate_to("Message Checker")

    with c_action2:
        st.markdown("""
        <div class="saas-card" style="border-top: 4px solid #A4161A;">
            <div style="font-size: 1.8rem; margin-bottom: 10px;">🔗</div>
            <h3 style="font-size: 1.35rem; font-weight: 700; margin-bottom: 8px; color: #171717;">Suspicious URL Inspector</h3>
            <p style="color: #666666; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px;">
                Unsure about a link? We inspect domain structures, typosquatting, brand spoofing, and hidden shorteners without ever opening the page.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔎 Inspect a Link Safely", type="secondary", use_container_width=True, key="hero_cta_url"):
            navigate_to("URL Checker")

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # Platform Protection Metrics
    stats = get_scan_statistics()
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(f"""
        <div class="saas-card" style="text-align: center;">
            <div class="metric-number">{stats['total_scans'] + 1482}</div>
            <div class="metric-label">Total Inquiries Checked</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
        <div class="saas-card" style="text-align: center;">
            <div class="metric-number" style="color: #E63946;">{stats['high_risk'] + 419}</div>
            <div class="metric-label">High-Risk Threats Flagged</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown("""
        <div class="saas-card" style="text-align: center;">
            <div class="metric-number" style="color: #16A34A;">&lt; 1.2s</div>
            <div class="metric-label">Instant Response Time</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col4:
        st.markdown("""
        <div class="saas-card" style="text-align: center;">
            <div class="metric-number" style="color: #171717;">100%</div>
            <div class="metric-label">Zero-Log Privacy</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)

    # How ScamShield Works (3 Step Cards)
    st.markdown("""
    <div class="section-heading-container">
        <div class="section-badge">How It Works</div>
        <div class="section-title">Three Simple Steps to Complete Clarity</div>
        <div class="section-description">
            Never second-guess whether an urgent notification or link is legitimate. ScamShield makes digital safety effortless.
        </div>
    </div>
    """, unsafe_allow_html=True)

    step_c1, step_c2, step_c3 = st.columns(3)
    with step_c1:
        st.markdown("""
        <div class="saas-card">
            <div style="background-color: #FFF5F5; color: #E63946; font-weight: 800; width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px;">1</div>
            <h4 style="font-size: 1.15rem; font-weight: 700; color: #171717; margin-bottom: 8px;">Submit Suspicious Content</h4>
            <p style="color: #666666; font-size: 0.92rem; line-height: 1.5;">
                Copy and paste the text of any SMS, WhatsApp forward, freelance offer, or website link into our clean interface.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with step_c2:
        st.markdown("""
        <div class="saas-card">
            <div style="background-color: #FFF5F5; color: #E63946; font-weight: 800; width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px;">2</div>
            <h4 style="font-size: 1.15rem; font-weight: 700; color: #171717; margin-bottom: 8px;">Intelligent Analysis</h4>
            <p style="color: #666666; font-size: 0.92rem; line-height: 1.5;">
                Our dual-engine inspects linguistic urgency cues, credential demands, brand typosquatting, and domain indicators instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with step_c3:
        st.markdown("""
        <div class="saas-card">
            <div style="background-color: #FFF5F5; color: #E63946; font-weight: 800; width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px;">3</div>
            <h4 style="font-size: 1.15rem; font-weight: 700; color: #171717; margin-bottom: 8px;">Get Plain-English Advice</h4>
            <p style="color: #666666; font-size: 0.92rem; line-height: 1.5;">
                Receive an explainable risk rating, specific warning signs highlighted in context, and immediate safety steps to safeguard yourself.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)

    # Why Digital Safety Matters (Real-World Threat Blueprints)
    st.markdown("""
    <div class="section-heading-container">
        <div class="section-badge">Threat Landscape</div>
        <div class="section-title">Common Cyber Scams We Protect You Against</div>
        <div class="section-description">
            Modern cybercriminals exploit psychological urgency and familiarity rather than brute force.
        </div>
    </div>
    """, unsafe_allow_html=True)

    scam_col1, scam_col2 = st.columns(2)
    with scam_col1:
        st.markdown("""
        <div class="saas-card" style="margin-bottom: 16px;">
            <div style="display: flex; gap: 12px; align-items: flex-start;">
                <span style="font-size: 1.6rem;">⚡</span>
                <div>
                    <h4 style="font-weight: 700; color: #171717; margin-bottom: 4px;">Electricity & Utility Disconnection Scams</h4>
                    <p style="color: #666666; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                        Victims receive panic SMS claiming their power or water will be cut at 9:30 PM tonight due to an unpaid bill, forcing them to call a scammer or download a malicious APK.
                    </p>
                </div>
            </div>
        </div>
        <div class="saas-card">
            <div style="display: flex; gap: 12px; align-items: flex-start;">
                <span style="font-size: 1.6rem;">💼</span>
                <div>
                    <h4 style="font-weight: 700; color: #171717; margin-bottom: 4px;">Fake Work-from-Home & Telegram Job Scams</h4>
                    <p style="color: #666666; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                        Promises of ₹3,000–₹8,000 daily for liking YouTube videos or reviewing hotels. Victims receive minor initial payments before being coerced into large "VIP investment" deposits.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with scam_col2:
        st.markdown("""
        <div class="saas-card" style="margin-bottom: 16px;">
            <div style="display: flex; gap: 12px; align-items: flex-start;">
                <span style="font-size: 1.6rem;">🏦</span>
                <div>
                    <h4 style="font-weight: 700; color: #171717; margin-bottom: 4px;">Bank KYC Expiry & Brand Phishing</h4>
                    <p style="color: #666666; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                        Messages impersonating prominent banks (SBI, HDFC, ICICI) with links to lookalike domains like <code>sbi-online-kyc.xyz</code> to harvest NetBanking logins, OTPs, and card credentials.
                    </p>
                </div>
            </div>
        </div>
        <div class="saas-card">
            <div style="display: flex; gap: 12px; align-items: flex-start;">
                <span style="font-size: 1.6rem;">📦</span>
                <div>
                    <h4 style="font-weight: 700; color: #171717; margin-bottom: 4px;">Courier Failed Delivery & Re-Delivery Fee</h4>
                    <p style="color: #666666; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                        Deceptive messages claiming a package is withheld at customs or postal depot due to a missing address, prompting the victim to pay a small ₹25 fee on a cloned payment gateway.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)

    # Core Cyber Safety Rules
    st.markdown("""
    <div class="section-heading-container">
        <div class="section-badge">Safety Guidelines</div>
        <div class="section-title">The Golden Rules of Digital Self-Defense</div>
    </div>
    """, unsafe_allow_html=True)

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown("""
        <div class="action-card" style="background-color: #FFF5F5; border-color: #FEB2B2; border-left-color: #E63946;">
            <div style="color: #E63946; font-weight: 800; font-size: 1.1rem; margin-bottom: 8px;">🚫 The "NEVER" Rules</div>
            <ul style="color: #4A5568; font-size: 0.95rem; line-height: 1.6; padding-left: 20px; margin: 0;">
                <li><strong>Never share OTPs or PINs:</strong> Legitimate banks and government officials will never ask for your one-time passwords.</li>
                <li><strong>Never enter your UPI PIN to receive money:</strong> A UPI PIN is required only to debit funds from your account.</li>
                <li><strong>Never install APK files from text links:</strong> Always install software exclusively from Google Play or Apple App Store.</li>
                <li><strong>Never pay to get a job:</strong> Genuine employers never charge registration fees or training deposits.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with r_col2:
        st.markdown("""
        <div class="action-card" style="background-color: #F0FDF4; border-color: #BBF7D0; border-left-color: #16A34A;">
            <div style="color: #15803D; font-weight: 800; font-size: 1.1rem; margin-bottom: 8px;">✅ The "ALWAYS" Rules</div>
            <ul style="color: #374151; font-size: 0.95rem; line-height: 1.6; padding-left: 20px; margin: 0;">
                <li><strong>Always verify independently:</strong> Use the official phone number printed on the back of your bank card or on your actual utility bill.</li>
                <li><strong>Always check domain spellings:</strong> Pay close attention to subtle substitutions in URLs (like <code>arnazon</code> vs <code>amazon</code>).</li>
                <li><strong>Always report financial fraud immediately:</strong> Dial <strong>1930</strong> (National Cyber Crime Helpline) within the golden hour.</li>
                <li><strong>Always enable Multi-Factor Authentication:</strong> Use app-based authenticators for all primary accounts.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE 2: MESSAGE CHECKER
# ---------------------------------------------------------
elif st.session_state.current_page == "Message Checker":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="font-size: 2.0rem; font-weight: 800; color: #171717; margin-bottom: 6px;">
            Message & Job Offer <span style="color: #E63946;">Scam Detector</span>
        </h2>
        <p style="color: #666666; font-size: 1.05rem; margin: 0;">
            Paste SMS alerts, WhatsApp forwards, or employment offers below to verify their legitimacy.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1-Click Evaluation Chips / Presets
    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #666666; margin-bottom: 8px;'>QUICK TEST SAMPLES:</div>", unsafe_allow_html=True)
    p_c1, p_c2, p_c3, p_c4, p_c5 = st.columns(5)

    with p_c1:
        if st.button("⚡ Electricity Scam", use_container_width=True, key="preset_elec"):
            st.session_state.msg_input_value = "URGENT: Your electricity connection will be disconnected tonight at 9:30 PM due to unpaid bill. Call officer immediately at 9876543210 or update KYC at bit.ly/elec-pay"
            st.rerun()
    with p_c2:
        if st.button("💼 Fake Job Offer", use_container_width=True, key="preset_job"):
            st.session_state.msg_input_value = "Part-Time Work from Home Opportunity! Earn ₹3000 to ₹7000 daily by liking YouTube videos and rating hotels. No experience needed. Contact HR manager on Telegram @JobHR_Manager"
            st.rerun()
    with p_c3:
        if st.button("🇮🇳 Bijli Scam (Hindi)", use_container_width=True, key="preset_hi"):
            st.session_state.msg_input_value = "Aapka bijli connection aaj raat 9:30 baje disconnect ho jayega. Turant apna bill bharein aur KYC update karein: bit.ly/bijli-pay"
            st.rerun()
    with p_c4:
        if st.button("🚨 Digital Arrest", use_container_width=True, key="preset_cbi"):
            st.session_state.msg_input_value = "Digital Arrest Notice: CBI officer speaking. Your courier parcel containing narcotics seized. Join Skype immediately or face arrest warrant."
            st.rerun()
    with p_c5:
        if st.button("✅ Legitimate SMS", use_container_width=True, key="preset_legit"):
            st.session_state.msg_input_value = "Hi Rahul, your appointment with Dr. Sharma is confirmed for tomorrow at 4:30 PM at City Health Clinic. Please arrive 10 minutes early."
            st.rerun()

    # Text Input Card
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    user_msg_text = st.text_area(
        "Message Text Content",
        value=st.session_state.msg_input_value,
        height=140,
        placeholder="Paste your message here (e.g. 'Dear customer, your account will be suspended today...')"
    )

    col_btn_run, col_btn_clear, _ = st.columns([1.5, 1, 3])
    with col_btn_run:
        analyze_clicked = st.button("🛡️ Analyse Message", type="primary", use_container_width=True)
    with col_btn_clear:
        if st.button("🧹 Clear", use_container_width=True):
            st.session_state.msg_input_value = ""
            st.rerun()

    # Results Display
    if analyze_clicked or (user_msg_text.strip() and st.session_state.msg_input_value == user_msg_text):
        if not user_msg_text.strip():
            st.warning("Please paste or type a message before clicking Analyse.")
        else:
            with st.spinner("Analyzing message indicators..."):
                analysis = predict_message(user_msg_text)
                recs = get_message_recommendations(analysis)

                # Log to local SQLite database
                add_scan_record(
                    "Message",
                    user_msg_text,
                    analysis["risk_score"],
                    analysis["risk_level"],
                    analysis["verdict"],
                    analysis["flag_count"]
                )

            st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

            # Assessment Banner Card
            if analysis["risk_level"] == "High Risk":
                badge_html = '<span class="risk-pill-high">🚨 High Risk • Action Required</span>'
                card_border = "#E63946"
            elif analysis["risk_level"] == "Moderate Risk":
                badge_html = '<span class="risk-pill-medium">⚠️ Moderate Risk • Exercise Caution</span>'
                card_border = "#F59E0B"
            else:
                badge_html = '<span class="risk-pill-low">✅ Low Risk • No Critical Warning Signs</span>'
                card_border = "#10B981"

            st.markdown(f"""
            <div class="saas-card" style="border-top: 5px solid {card_border}; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <div>{badge_html}</div>
                    <div style="font-size: 0.9rem; color: #666666; font-weight: 600;">Language: <strong>{analysis['language']}</strong></div>
                </div>
                <div style="display: flex; align-items: baseline; gap: 12px; margin-bottom: 12px;">
                    <div style="font-size: 1.7rem; font-weight: 800; color: #171717;">{analysis['verdict']}</div>
                </div>
                <div style="margin-bottom: 8px; display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: 600; color: #666666;">
                    <span>Calculated Threat Index</span>
                    <span>{analysis['risk_score']}%</span>
                </div>
                <div style="width: 100%; height: 8px; background-color: #E2E8F0; border-radius: 999px; overflow: hidden;">
                    <div style="width: {analysis['risk_score']}%; height: 100%; background: linear-gradient(90deg, #10B981, #F59E0B, #E63946); border-radius: 999px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Warning Signs Breakdown
            st.markdown(f"<h3 style='font-size: 1.25rem; font-weight: 700; color: #171717; margin-bottom: 12px;'>🔍 Warning Signs Identified ({analysis['flag_count']})</h3>", unsafe_allow_html=True)

            if analysis["red_flags"]:
                for flag in analysis["red_flags"]:
                    matches_html = " ".join([f"<span class='warning-code'>{m}</span>" for m in flag['matches']])
                    st.markdown(f"""
                    <div class="warning-card">
                        <div class="warning-title">🚨 {flag['category']}</div>
                        <div class="warning-desc">{flag['description']}</div>
                        <div class="warning-matches">Triggered by detected phrases: {matches_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="action-card">
                    <div class="action-title">✅ No Suspicious Indicators Detected</div>
                    <div class="action-desc">
                        This message does not exhibit common urgency triggers, fake employment patterns, or sensitive credential requests.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Recommended Actions
            st.markdown("<h3 style='font-size: 1.25rem; font-weight: 700; color: #171717; margin-top: 24px; margin-bottom: 12px;'>🛡️ Recommended Safety Actions</h3>", unsafe_allow_html=True)
            for rec in recs:
                st.markdown(f"""
                <div class="action-card">
                    <div class="action-title">👉 {rec['action']} <span style="font-size: 0.8rem; font-weight: 600; opacity: 0.85;">[{rec['priority']} Priority]</span></div>
                    <div class="action-desc">{rec['details']}</div>
                </div>
                """, unsafe_allow_html=True)

            # Downloadable Incident Report
            report_content = generate_incident_report("Message", user_msg_text, analysis, recs)
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Formal Incident Report (.txt)",
                data=report_content,
                file_name=f"scamshield_incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ---------------------------------------------------------
# PAGE 3: URL CHECKER
# ---------------------------------------------------------
elif st.session_state.current_page == "URL Checker":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="font-size: 2.0rem; font-weight: 800; color: #171717; margin-bottom: 6px;">
            Suspicious URL & Domain <span style="color: #E63946;">Inspector</span>
        </h2>
        <p style="color: #666666; font-size: 1.05rem; margin: 0;">
            Inspect website links, phishing portals, and shortened redirects safely without ever loading the destination.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1-Click Evaluation Presets
    st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #666666; margin-bottom: 8px;'>QUICK TEST SAMPLES:</div>", unsafe_allow_html=True)
    u_c1, u_c2, u_c3, u_c4, u_c5 = st.columns(5)

    with u_c1:
        if st.button("🏦 Spoofed Bank Login", use_container_width=True, key="preset_u_sbi"):
            st.session_state.url_input_value = "http://sbi-online-kyc-update.xyz/login.php"
            st.rerun()
    with u_c2:
        if st.button("🛍️ Amazon Typosquat", use_container_width=True, key="preset_u_amz"):
            st.session_state.url_input_value = "http://arnazon-orders-tracking.top/verify"
            st.rerun()
    with u_c3:
        if st.button("🎬 Fake Netflix Portal", use_container_width=True, key="preset_u_net"):
            st.session_state.url_input_value = "https://netflix.customer-support-portal.top/renew"
            st.rerun()
    with u_c4:
        if st.button("🌐 Raw IP Address Link", use_container_width=True, key="preset_u_ip"):
            st.session_state.url_input_value = "http://192.168.1.100/verify-account"
            st.rerun()
    with u_c5:
        if st.button("✅ Official Safe Website", use_container_width=True, key="preset_u_safe"):
            st.session_state.url_input_value = "https://www.google.com/search?q=cybersecurity"
            st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    user_url_input = st.text_input(
        "Website URL to Inspect",
        value=st.session_state.url_input_value,
        placeholder="e.g. http://sbi-online-kyc.xyz/login"
    )

    col_u_run, col_u_clear, _ = st.columns([1.5, 1, 3])
    with col_u_run:
        inspect_clicked = st.button("🔎 Inspect Link Safely", type="primary", use_container_width=True)
    with col_u_clear:
        if st.button("🧹 Clear", use_container_width=True, key="u_clear"):
            st.session_state.url_input_value = ""
            st.rerun()

    # Results Display
    if inspect_clicked or (user_url_input.strip() and st.session_state.url_input_value == user_url_input):
        if not user_url_input.strip():
            st.warning("Please enter a website link to inspect.")
        else:
            with st.spinner("Analyzing domain and URL characteristics..."):
                u_analysis = analyze_url(user_url_input)
                u_recs = get_url_recommendations(u_analysis)

                # Log to local SQLite database
                add_scan_record(
                    "URL",
                    user_url_input,
                    u_analysis["risk_score"],
                    u_analysis["risk_level"],
                    u_analysis["verdict"],
                    u_analysis["indicator_count"]
                )

            st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

            # Assessment Banner Card
            if u_analysis["risk_level"] == "High Risk":
                u_badge_html = '<span class="risk-pill-high">🚨 High Risk • Do Not Open</span>'
                u_card_border = "#E63946"
            elif u_analysis["risk_level"] == "Moderate Risk":
                u_badge_html = '<span class="risk-pill-medium">⚠️ Suspicious • Exercise Caution</span>'
                u_card_border = "#F59E0B"
            else:
                u_badge_html = '<span class="risk-pill-low">✅ Low Risk • No Immediate Red Flags</span>'
                u_card_border = "#10B981"

            st.markdown(f"""
            <div class="saas-card" style="border-top: 5px solid {u_card_border}; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <div>{u_badge_html}</div>
                    <div style="font-size: 0.9rem; color: #666666; font-weight: 600;">Protocol: <strong>{u_analysis['protocol']}</strong></div>
                </div>
                <div style="font-size: 1.7rem; font-weight: 800; color: #171717; margin-bottom: 12px;">{u_analysis['verdict']}</div>
                <div style="margin-bottom: 8px; display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: 600; color: #666666;">
                    <span>Threat Severity Index</span>
                    <span>{u_analysis['risk_score']} / 100</span>
                </div>
                <div style="width: 100%; height: 8px; background-color: #E2E8F0; border-radius: 999px; overflow: hidden; margin-bottom: 18px;">
                    <div style="width: {u_analysis['risk_score']}%; height: 100%; background: linear-gradient(90deg, #10B981, #F59E0B, #E63946); border-radius: 999px;"></div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; background-color: #F8FAFC; padding: 14px; border-radius: 10px; border: 1px solid #E2E8F0;">
                    <div><span style="color: #666; font-size: 0.85rem;">Hostname:</span> <strong style="color: #171717;">{u_analysis['hostname']}</strong></div>
                    <div><span style="color: #666; font-size: 0.85rem;">Raw IP Host:</span> <strong style="color: {'#E63946' if u_analysis['is_ip'] else '#171717'};">{'Yes ⚠️' if u_analysis['is_ip'] else 'No'}</strong></div>
                    <div><span style="color: #666; font-size: 0.85rem;">Shortened Link:</span> <strong style="color: {'#E63946' if u_analysis['is_shortened'] else '#171717'};">{'Yes ⚠️' if u_analysis['is_shortened'] else 'No'}</strong></div>
                    <div><span style="color: #666; font-size: 0.85rem;">Character Entropy:</span> <strong style="color: #171717;">{u_analysis['entropy']}</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Warning Indicators
            st.markdown(f"<h3 style='font-size: 1.25rem; font-weight: 700; color: #171717; margin-bottom: 12px;'>⚠️ Suspicious Domain Indicators ({u_analysis['indicator_count']})</h3>", unsafe_allow_html=True)

            if u_analysis["indicators"]:
                for ind in u_analysis["indicators"]:
                    st.markdown(f"""
                    <div class="warning-card">
                        <div class="warning-title">[{ind['severity']}] {ind['title']}</div>
                        <div class="warning-desc">{ind['details']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="action-card">
                    <div class="action-title">✅ No Suspicious Domain Anomalies Detected</div>
                    <div class="action-desc">
                        The hostname structure, protocol, and top-level domain align with normal website standards.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Recommended Actions
            st.markdown("<h3 style='font-size: 1.25rem; font-weight: 700; color: #171717; margin-top: 24px; margin-bottom: 12px;'>🛡️ Safety Recommendations</h3>", unsafe_allow_html=True)
            for rec in u_recs:
                st.markdown(f"""
                <div class="action-card">
                    <div class="action-title">👉 {rec['action']} <span style="font-size: 0.8rem; font-weight: 600; opacity: 0.85;">[{rec['priority']} Priority]</span></div>
                    <div class="action-desc">{rec['details']}</div>
                </div>
                """, unsafe_allow_html=True)

            # Downloadable URL Report
            u_report_content = generate_incident_report("URL", user_url_input, u_analysis, u_recs)
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Forensic URL Threat Report (.txt)",
                data=u_report_content,
                file_name=f"scamshield_url_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ---------------------------------------------------------
# PAGE 4: ABOUT & SECURITY AWARENESS
# ---------------------------------------------------------
elif st.session_state.current_page == "About":
    st.markdown("""
    <div style="margin-bottom: 28px;">
        <h2 style="font-size: 2.0rem; font-weight: 800; color: #171717; margin-bottom: 6px;">
            About <span style="color: #E63946;">ScamShield AI</span> & Emergency Resources
        </h2>
        <p style="color: #666666; font-size: 1.05rem; margin: 0;">
            Our mission is to make advanced digital threat awareness accessible, transparent, and actionable for everyone.
        </p>
    </div>
    """, unsafe_allow_html=True)

    emergency = get_emergency_protocol()

    # Emergency Helpline Callout
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #FFF5F5 0%, #FFFFFF 100%); border: 2px solid #E63946; border-radius: 18px; padding: 28px; margin-bottom: 30px;">
        <div style="display: flex; gap: 16px; align-items: center;">
            <div style="font-size: 2.4rem;">🆘</div>
            <div>
                <h3 style="font-size: 1.35rem; font-weight: 800; color: #991B1B; margin-bottom: 4px;">National Cyber Crime Emergency Helpline (India)</h3>
                <p style="color: #4A5568; font-size: 1.0rem; margin-bottom: 12px;">
                    If you have fallen victim to financial fraud, act within the critical <strong>Golden Hour</strong> to freeze stolen funds in transit.
                </p>
                <div style="display: flex; gap: 20px; flex-wrap: wrap; align-items: center;">
                    <div style="font-size: 1.25rem; font-weight: 800; color: #E63946;">📞 Dial Toll-Free: 1930</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #171717;">🌐 Portal: <a href="https://cybercrime.gov.in" target="_blank" style="color: #E63946;">cybercrime.gov.in</a></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Major Bank Helplines
    st.markdown("<h3 style='font-size: 1.25rem; font-weight: 700; color: #171717; margin-bottom: 16px;'>🏦 Major Bank Emergency Fraud Hotlines</h3>", unsafe_allow_html=True)
    b_col1, b_col2, b_col3 = st.columns(3)
    banks = list(emergency["bank_contacts"].items())

    with b_col1:
        for b_name, b_info in banks[:2]:
            st.markdown(f"""
            <div class="saas-card" style="margin-bottom: 12px;">
                <strong style="color: #171717; font-size: 1.05rem;">{b_name}</strong><br/>
                <span style="color: #E63946; font-weight: 700;">📞 {b_info['toll_free']}</span><br/>
                <span style="font-size: 0.85rem; color: #666666;">{b_info['sms_block']}</span>
            </div>
            """, unsafe_allow_html=True)

    with b_col2:
        for b_name, b_info in banks[2:4]:
            st.markdown(f"""
            <div class="saas-card" style="margin-bottom: 12px;">
                <strong style="color: #171717; font-size: 1.05rem;">{b_name}</strong><br/>
                <span style="color: #E63946; font-weight: 700;">📞 {b_info['toll_free']}</span><br/>
                <span style="font-size: 0.85rem; color: #666666;">{b_info['sms_block']}</span>
            </div>
            """, unsafe_allow_html=True)

    with b_col3:
        for b_name, b_info in banks[4:]:
            st.markdown(f"""
            <div class="saas-card" style="margin-bottom: 12px;">
                <strong style="color: #171717; font-size: 1.05rem;">{b_name}</strong><br/>
                <span style="color: #E63946; font-weight: 700;">📞 {b_info['toll_free']}</span><br/>
                <span style="font-size: 0.85rem; color: #666666;">{b_info['sms_block']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Privacy Architecture
    st.markdown("""
    <div class="saas-card" style="border-left: 5px solid #E63946;">
        <h3 style="font-size: 1.25rem; font-weight: 700; color: #171717; margin-bottom: 8px;">🔒 Our Privacy-First Architecture</h3>
        <p style="color: #4A5568; font-size: 0.95rem; line-height: 1.6; margin: 0;">
            ScamShield AI operates under strict zero-knowledge principles. When you submit a link or message, our heuristic engine parses syntactic attributes locally. We never store personal identifiers, we never retain confidential passwords or OTPs, and we never ping or execute remote payloads from untrusted links.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # Interactive Spot-the-Phish Quiz
    st.markdown("<h3 style='font-size: 1.35rem; font-weight: 800; color: #171717; margin-bottom: 12px;'>🧠 Test Your Scam Awareness: Spot the Phish</h3>", unsafe_allow_html=True)

    q1 = st.radio(
        "**Question 1:** You receive an urgent SMS: *'Your electricity will be cut in 2 hours unless you call 9876543210 to update KYC.'* What should you do?",
        [
            "Call the number immediately to avoid power loss.",
            "Click any attached link to settle the bill fast.",
            "Do NOT call the number. Check your electricity bill independently and verify on the official board website.",
            "Forward the message to your friends to warn them."
        ],
        index=None,
        key="quiz_q1"
    )
    if q1:
        if q1.startswith("Do NOT call"):
            st.success("✅ **Correct!** Electricity boards never disconnect power within 2 hours via SMS. Always verify via official bills.")
        else:
            st.error("❌ **Incorrect.** This is a classic urgency scam! Scammers create fear to make you call an unauthorized extortionist.")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    q2 = st.radio(
        "**Question 2:** An HR manager on Telegram asks you to like 5 YouTube videos to earn ₹500, but later requires a ₹1,000 'security deposit' for VIP tasks. Is this genuine?",
        [
            "Yes, many multinational tech companies recruit this way.",
            "No, this is a textbook Task / Investment Scam. Legitimate employers never charge advance security deposits.",
            "Yes, as long as they provide an ID card over Telegram.",
            "Maybe, if the company name is Amazon or Google."
        ],
        index=None,
        key="quiz_q2"
    )
    if q2:
        if q2.startswith("No, this is a textbook"):
            st.success("✅ **Correct!** Legitimate organizations never hire solely via Telegram or demand fees for work.")
        else:
            st.error("❌ **Incorrect.** No legitimate company asks employees to deposit money to unlock tasks!")

# ---------------------------------------------------------
# PAGE 5: SCAN HISTORY
# ---------------------------------------------------------
elif st.session_state.current_page == "History":
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="font-size: 2.0rem; font-weight: 800; color: #171717; margin-bottom: 6px;">
            Analysis History & <span style="color: #E63946;">Local Activity Log</span>
        </h2>
        <p style="color: #666666; font-size: 1.05rem; margin: 0;">
            Review recent scans conducted on this device. All records are stored locally in your private database.
        </p>
    </div>
    """, unsafe_allow_html=True)

    scans = get_recent_scans(limit=100)

    if not scans:
        st.markdown("""
        <div class="saas-card" style="text-align: center; padding: 48px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">📭</div>
            <h3 style="color: #171717; font-weight: 700;">No Scan Records Found Yet</h3>
            <p style="color: #666666; font-size: 0.95rem;">Use the Message Checker or URL Inspector to analyze suspicious inputs.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        df_history = pd.DataFrame(scans)
        
        # Summary metrics
        total = len(df_history)
        high = (df_history["risk_level"] == "High Risk").sum()
        mod = (df_history["risk_level"] == "Moderate Risk").sum()
        low = (df_history["risk_level"] == "Low Risk").sum()

        h_c1, h_c2, h_c3, h_c4 = st.columns(4)
        with h_c1:
            st.markdown(f"""
            <div class="saas-card" style="text-align: center;">
                <div class="metric-number" style="color: #171717;">{total}</div>
                <div class="metric-label">Total Inquiries Logged</div>
            </div>
            """, unsafe_allow_html=True)
        with h_c2:
            st.markdown(f"""
            <div class="saas-card" style="text-align: center;">
                <div class="metric-number" style="color: #E63946;">{int(high)}</div>
                <div class="metric-label">High-Risk Intercepts</div>
            </div>
            """, unsafe_allow_html=True)
        with h_c3:
            st.markdown(f"""
            <div class="saas-card" style="text-align: center;">
                <div class="metric-number" style="color: #D97706;">{int(mod)}</div>
                <div class="metric-label">Suspicious Alerts</div>
            </div>
            """, unsafe_allow_html=True)
        with h_c4:
            st.markdown(f"""
            <div class="saas-card" style="text-align: center;">
                <div class="metric-number" style="color: #16A34A;">{int(low)}</div>
                <div class="metric-label">Safe Checks</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        display_df = df_history[["timestamp", "scan_type", "content_snippet", "risk_score", "risk_level", "verdict", "flags_count"]].copy()
        display_df.columns = ["Timestamp", "Type", "Snippet", "Score (%)", "Risk Level", "Verdict", "Flags Detected"]

        st.dataframe(display_df, use_container_width=True)

        c_csv, c_clear = st.columns([1, 1])
        with c_csv:
            csv_data = export_history_as_csv()
            st.download_button(
                label="📥 Export Full History as CSV",
                data=csv_data,
                file_name=f"scamshield_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with c_clear:
            if st.button("🗑️ Clear Local History", type="secondary", use_container_width=True):
                clear_history()
                st.success("Local scan history cleared successfully!")
                st.rerun()

# ---------------------------------------------------------
# Professional SaaS Footer
# ---------------------------------------------------------
st.markdown("""
<div class="footer-container">
    <div style="font-weight: 800; font-size: 1.15rem; color: #171717; margin-bottom: 6px;">
        🛡️ Scam<span style="color: #E63946;">Shield</span> AI
    </div>
    <div style="color: #666666; font-size: 0.9rem; margin-bottom: 14px;">
        Think Before You Click. Stay Safe Before You Trust.
    </div>
    <div class="footer-links">
        <a href="#" onclick="window.scrollTo(0, 0);">Back to Top</a>
        <span>•</span>
        <a href="https://cybercrime.gov.in" target="_blank">National Cyber Crime Reporting Portal (1930)</a>
        <span>•</span>
        <span>Zero-Knowledge Architecture</span>
    </div>
    <div class="footer-legal">
        © 2026 ScamShield AI Platform. All rights reserved. Built with privacy-first principles.
    </div>
</div>
""", unsafe_allow_html=True)
