import React, { useState } from 'react';
import { AlertCircle, ShieldAlert, CheckCircle2, Download, RefreshCw, Send } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || '';

export default function MessageChecker() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const presets = [
    {
      label: '⚡ Electricity Scam',
      text: 'URGENT: Your electricity connection will be disconnected tonight at 9:30 PM due to unpaid bill. Call officer immediately at 9876543210 or update KYC at bit.ly/elec-pay'
    },
    {
      label: '💼 Fake Job Offer',
      text: 'Part-Time Work from Home Opportunity! Earn ₹3000 to ₹7000 daily by liking YouTube videos and rating hotels. No experience needed. Contact HR manager on Telegram @JobHR_Manager'
    },
    {
      label: '🇮🇳 Bijli Scam (Hindi)',
      text: 'Aapka bijli connection aaj raat 9:30 baje disconnect ho jayega. Turant apna bill bharein aur KYC update karein: bit.ly/bijli-pay'
    },
    {
      label: '🚨 Digital Arrest',
      text: 'Digital Arrest Notice: CBI officer speaking. Your courier parcel containing narcotics seized. Join Skype immediately or face non-bailable arrest warrant.'
    },
    {
      label: '✅ Legitimate SMS',
      text: 'Hi Rahul, your appointment with Dr. Sharma is confirmed for tomorrow at 4:30 PM at City Health Clinic. Please arrive 10 minutes early.'
    }
  ];

  const handleAnalyze = async () => {
    if (!message.trim()) {
      setError('Please enter or paste a message to analyze.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/api/analyze-message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message.trim() })
      });

      if (!response.ok) {
        throw new Error(`Server returned error code ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError('Could not reach backend API. Ensure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = () => {
    if (!result?.report) return;
    const blob = new Blob([result.report], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `scamshield_report_${Date.now()}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="container" style={{ paddingTop: '32px', paddingBottom: '60px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '2.0rem', fontWeight: 800, color: '#171717', marginBottom: '6px' }}>
          Message & Job Offer <span style={{ color: '#E63946' }}>Scam Detector</span>
        </h2>
        <p style={{ color: '#666666', fontSize: '1.05rem', margin: 0 }}>
          Paste SMS alerts, WhatsApp forwards, or employment offers below to verify their legitimacy.
        </p>
      </div>

      {/* Preset Chips */}
      <div style={{ marginBottom: '16px' }}>
        <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#666666', marginBottom: '8px' }}>
          QUICK TEST SAMPLES:
        </div>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {presets.map((p, idx) => (
            <button
              key={idx}
              className="btn-secondary"
              style={{ padding: '6px 14px', fontSize: '0.85rem' }}
              onClick={() => {
                setMessage(p.text);
                setError(null);
              }}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Input Form */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <textarea
          rows={5}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Paste suspicious SMS, WhatsApp message, or job offer here..."
          style={{ marginBottom: '16px' }}
        />

        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <button
            className="btn-primary"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? <RefreshCw className="animate-spin" size={18} /> : <Send size={18} />}
            {loading ? 'Analyzing Message...' : 'Analyse Message'}
          </button>
          <button
            className="btn-secondary"
            onClick={() => {
              setMessage('');
              setResult(null);
              setError(null);
            }}
          >
            Clear
          </button>
        </div>

        {error && (
          <div style={{ marginTop: '16px', color: '#DC2626', fontWeight: 600, fontSize: '0.92rem' }}>
            ⚠️ {error}
          </div>
        )}
      </div>

      {/* Results Section */}
      {result && result.analysis && (
        <div style={{ marginTop: '30px' }}>
          {/* Verdict Banner Card */}
          <div
            className="card"
            style={{
              borderTop: `5px solid ${
                result.analysis.risk_level === 'High Risk'
                  ? '#E63946'
                  : result.analysis.risk_level === 'Moderate Risk'
                  ? '#F59E0B'
                  : '#10B981'
              }`,
              marginBottom: '24px'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
              <span
                className={
                  result.analysis.risk_level === 'High Risk'
                    ? 'badge-high'
                    : result.analysis.risk_level === 'Moderate Risk'
                    ? 'badge-medium'
                    : 'badge-low'
                }
              >
                {result.analysis.risk_level === 'High Risk' && <ShieldAlert size={14} />}
                {result.analysis.risk_level === 'Moderate Risk' && <AlertCircle size={14} />}
                {result.analysis.risk_level === 'Low Risk' && <CheckCircle2 size={14} />}
                {result.analysis.risk_level} • Threat Rating
              </span>

              <span style={{ fontSize: '0.85rem', color: '#666666', fontWeight: 600 }}>
                Language: <strong>{result.analysis.language}</strong>
              </span>
            </div>

            <h3 style={{ fontSize: '1.65rem', fontWeight: 800, color: '#171717', marginBottom: '10px' }}>
              {result.analysis.verdict}
            </h3>

            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', fontWeight: 600, color: '#666666', marginBottom: '4px' }}>
              <span>Calculated Threat Index</span>
              <span>{result.analysis.risk_score}%</span>
            </div>
            <div className="progress-container">
              <div className="progress-bar" style={{ width: `${result.analysis.risk_score}%` }}></div>
            </div>
          </div>

          {/* Warning Signs */}
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '14px' }}>
            🔍 Warning Signs Identified ({result.analysis.flag_count})
          </h3>

          {result.analysis.red_flags && result.analysis.red_flags.length > 0 ? (
            result.analysis.red_flags.map((flag, idx) => (
              <div key={idx} className="warning-box">
                <div style={{ color: '#A4161A', fontWeight: 700, fontSize: '1.05rem', marginBottom: '4px' }}>
                  🚨 {flag.category}
                </div>
                <div style={{ color: '#4A5568', fontSize: '0.95rem' }}>{flag.description}</div>
                {flag.matches && flag.matches.length > 0 && (
                  <div style={{ color: '#718096', fontSize: '0.85rem', marginTop: '6px' }}>
                    Triggered by detected phrases:{' '}
                    {flag.matches.map((m, mIdx) => (
                      <span
                        key={mIdx}
                        style={{
                          backgroundColor: '#FFFFFF',
                          border: '1px solid #E2E8F0',
                          padding: '2px 6px',
                          borderRadius: '4px',
                          color: '#C53030',
                          fontWeight: 600,
                          marginRight: '4px'
                        }}
                      >
                        {m}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="action-box">
              <div style={{ color: '#15803D', fontWeight: 700 }}>✅ No Critical Linguistic Scam Indicators</div>
              <div style={{ color: '#374151', fontSize: '0.95rem' }}>
                This message does not exhibit artificial urgency, fake employment promises, or sensitive credential harvesting.
              </div>
            </div>
          )}

          {/* Recommendations */}
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginTop: '28px', marginBottom: '14px' }}>
            🛡️ Recommended Safety Actions
          </h3>

          {result.recommendations &&
            result.recommendations.map((rec, rIdx) => (
              <div key={rIdx} className="action-box">
                <div style={{ color: '#15803D', fontWeight: 700, fontSize: '1.05rem', marginBottom: '4px' }}>
                  👉 {rec.action}{' '}
                  <span style={{ fontSize: '0.8rem', fontWeight: 600, opacity: 0.85 }}>
                    [{rec.priority} Priority]
                  </span>
                </div>
                <div style={{ color: '#374151', fontSize: '0.95rem' }}>{rec.details}</div>
              </div>
            ))}

          {/* Download Forensic Report Button */}
          <div style={{ marginTop: '24px' }}>
            <button className="btn-secondary" onClick={handleDownloadReport} style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
              <Download size={18} />
              Download Formal Forensic Incident Report (.txt)
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
