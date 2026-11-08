"""
ScamShield AI - High-Performance FastAPI Backend Server
Provides RESTful API endpoints for Message Scam Analysis, URL Threat Intelligence,
and Forensic Report Generation for the React/Netlify Frontend.
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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

# Initialize Database
init_db()

app = FastAPI(
    title="ScamShield AI API",
    description="Cybersecurity Threat Detection Engine for SMS, WhatsApp, and URL phishing.",
    version="2.0.0"
)

# Enable CORS for Netlify frontend and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for seamless Netlify integration
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Request & Response Schemas
# ---------------------------------------------------------
class MessageRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Message text to analyze")

class UrlRequest(BaseModel):
    url: str = Field(..., min_length=1, description="Target URL or domain to inspect")
    api_key: Optional[str] = Field(None, description="Optional VirusTotal API key")

# ---------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------
@app.get("/")
def health_check():
    """Root endpoint for Render health checks and API discovery."""
    return {
        "status": "online",
        "service": "ScamShield AI Detection Engine",
        "version": "2.0.0",
        "architecture": "Hybrid Machine Learning + Heuristic Rule Extractor",
        "documentation": "/docs"
    }

@app.post("/api/analyze-message")
def analyze_message_endpoint(req: MessageRequest):
    """
    Analyzes an input message for smishing, job fraud, artificial urgency,
    credential requests, and returns explainable indicators with safety actions.
    """
    text = req.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Message text cannot be empty.")

    try:
        analysis = predict_message(text)
        recs = get_message_recommendations(analysis)

        # Log scan locally in SQLite
        add_scan_record(
            "Message",
            text,
            analysis["risk_score"],
            analysis["risk_level"],
            analysis["verdict"],
            analysis["flag_count"]
        )

        # Generate downloadable forensic report
        report_text = generate_incident_report("Message", text, analysis, recs)

        return {
            "success": True,
            "analysis": analysis,
            "recommendations": recs,
            "report": report_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/analyze-url")
def analyze_url_endpoint(req: UrlRequest):
    """
    Safely inspects a URL for typosquatting, brand impersonation,
    raw IP usage, suspicious TLDs, and high Shannon entropy without opening the URL.
    """
    target_url = req.url.strip()
    if not target_url:
        raise HTTPException(status_code=400, detail="Target URL cannot be empty.")

    try:
        u_analysis = analyze_url(target_url, req.api_key)
        u_recs = get_url_recommendations(u_analysis)

        # Log scan locally in SQLite
        add_scan_record(
            "URL",
            target_url,
            u_analysis["risk_score"],
            u_analysis["risk_level"],
            u_analysis["verdict"],
            u_analysis["indicator_count"]
        )

        # Generate downloadable forensic report
        u_report_text = generate_incident_report("URL", target_url, u_analysis, u_recs)

        return {
            "success": True,
            "analysis": u_analysis,
            "recommendations": u_recs,
            "report": u_report_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL inspection failed: {str(e)}")

@app.get("/api/history")
def get_history_endpoint(limit: int = 50):
    """Returns past scan history and summary metrics from SQLite."""
    try:
        stats = get_scan_statistics()
        recent = get_recent_scans(limit=limit)
        return {
            "success": True,
            "stats": stats,
            "history": recent
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

@app.delete("/api/history")
def clear_history_endpoint():
    """Clears all scan history from SQLite."""
    try:
        clear_history()
        return {"success": True, "message": "Scan history cleared successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database clear failed: {str(e)}")

@app.get("/api/history/export")
def export_history_endpoint():
    """Exports all scan records as CSV string."""
    try:
        csv_data = export_history_as_csv()
        return {"success": True, "csv": csv_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV export failed: {str(e)}")

@app.get("/api/emergency-contacts")
def emergency_contacts_endpoint():
    """Returns official cybercrime emergency hotlines and bank fraud contacts."""
    return {
        "success": True,
        "protocol": get_emergency_protocol()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

