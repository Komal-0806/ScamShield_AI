"""
ScamShield AI - Local SQLite History & Analytics Module
Stores scan logs locally for privacy-preserving user review and statistical metrics.
"""

import os
import sqlite3
from datetime import datetime

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "scamshield.db")

def get_connection():
    """Returns a SQLite connection to the local database."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database table if it doesn't already exist."""
    conn = get_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                content_snippet TEXT NOT NULL,
                risk_score REAL NOT NULL,
                risk_level TEXT NOT NULL,
                verdict TEXT NOT NULL,
                flags_count INTEGER NOT NULL
            )
        """)
    conn.close()

def add_scan_record(scan_type: str, content: str, risk_score: float, risk_level: str, verdict: str, flags_count: int):
    """
    Saves a scan record. Truncates content snippet for privacy.
    """
    init_db()
    # Mask / truncate snippet to avoid storing long sensitive text
    snippet = content.strip().replace("\n", " ")
    if len(snippet) > 80:
        snippet = snippet[:77] + "..."

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    try:
        with conn:
            conn.execute("""
                INSERT INTO scan_history (
                    timestamp, scan_type, content_snippet, risk_score, risk_level, verdict, flags_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (current_time, scan_type, snippet, risk_score, risk_level, verdict, flags_count))
    finally:
        conn.close()

def get_recent_scans(limit: int = 50):
    """Returns recent scan records as a list of dictionaries."""
    init_db()
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, scan_type, content_snippet, risk_score, risk_level, verdict, flags_count
            FROM scan_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def clear_history():
    """Deletes all scan history records from the database."""
    init_db()
    conn = get_connection()
    try:
        with conn:
            conn.execute("DELETE FROM scan_history")
    finally:
        conn.close()

def get_scan_statistics():
    """Computes basic analytics for the dashboard metrics."""
    init_db()
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM scan_history")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk_level = 'High Risk'")
        high_risk = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk_level = 'Moderate Risk'")
        moderate_risk = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scan_history WHERE risk_level = 'Low Risk'")
        low_risk = cursor.fetchone()[0]

        return {
            "total_scans": total,
            "high_risk": high_risk,
            "moderate_risk": moderate_risk,
            "low_risk": low_risk
        }
    finally:
        conn.close()

def export_history_as_csv() -> str:
    """Exports all scan history records formatted as CSV string."""
    scans = get_recent_scans(limit=1000)
    if not scans:
        return ""
    import io
    import csv
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "timestamp", "scan_type", "content_snippet", "risk_score", "risk_level", "verdict", "flags_count"])
    writer.writeheader()
    writer.writerows(scans)
    return output.getvalue()


