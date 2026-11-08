import React, { useState } from 'react';
import { Search, ShieldAlert, AlertCircle, CheckCircle2, Download, RefreshCw } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || '';

export default function UrlChecker() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const presets = [
    {
      label: '🏦 Spoofed Bank Login',
      link: 'http://sbi-online-kyc-update.xyz/login.php'
    },
    {
      label: '🛍️ Amazon Typosquat',
      link: 'http://arnazon-orders-tracking.top/verify'
    },
    {
      label: '🎬 Fake Netflix Subscription',
      link: 'https://netflix.customer-support-portal.top/renew'
    },
    {
      label: '🌐 Raw IP Address Link',
      link: 'http://192.168.1.100/verify-account'
    },
    {
      label: '✅ Official Safe Site',
      link: 'https://www.google.com/search?q=cybersecurity'
    }
  ];

  const handleInspect = async () => {
    if (!url.trim()) {
      setError('Please enter a website link to inspect.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/api/analyze-url`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url.trim() })
      });

      if (!response.ok) {
        throw new Error(`Server returned status code ${response.status}`);
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
    const blobUrl = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = `scamshield_url_report_${Date.now()}.txt`;
    link.click();
    URL.revokeObjectURL(blobUrl);
  };

  return (
    <div className="container" style={{ paddingTop: '32px', paddingBottom: '60px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '2.0rem', fontWeight: 800, color: '#171717', marginBottom: '6px' }}>
          Suspicious URL & Domain <span style={{ color: '#E63946' }}>Inspector</span>
        </h2>
        <p style={{ color: '#666666', fontSize: '1.05rem', margin: 0 }}>
          Inspect website links, phishing portals, and shortened redirects safely without ever loading the destination.
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
                setUrl(p.link);
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
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste or type website URL (e.g. http://sbi-online-kyc.xyz/login)"
          style={{ marginBottom: '16px' }}
        />

        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <button
            className="btn-primary"
            onClick={handleInspect}
            disabled={loading}
          >
            {loading ? <RefreshCw className="animate-spin" size={18} /> : <Search size={18} />}
            {loading ? 'Inspecting Link...' : 'Inspect Link Safely'}
          </button>
          <button
            className="btn-secondary"
            onClick={() => {
              setUrl('');
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
                {result.analysis.risk_level} • Security Assessment
              </span>

              <span style={{ fontSize: '0.85rem', color: '#666666', fontWeight: 600 }}>
                Protocol: <strong>{result.analysis.protocol}</strong>
              </span>
            </div>

            <h3 style={{ fontSize: '1.65rem', fontWeight: 800, color: '#171717', marginBottom: '10px' }}>
              {result.analysis.verdict}
            </h3>

            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', fontWeight: 600, color: '#666666', marginBottom: '4px' }}>
              <span>Threat Severity Index</span>
              <span>{result.analysis.risk_score} / 100</span>
            </div>
            <div className="progress-container" style={{ marginBottom: '18px' }}>
              <div className="progress-bar" style={{ width: `${result.analysis.risk_score}%` }}></div>
            </div>

            {/* Structural Breakdown Grid */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '12px',
              backgroundColor: '#F8FAFC',
              padding: '14px',
              borderRadius: '10px',
              border: '1px solid #E2E8F0'
            }}>
              <div>
                <span style={{ color: '#666', fontSize: '0.85rem' }}>Hostname:</span>{' '}
                <strong style={{ color: '#171717' }}>{result.analysis.hostname}</strong>
              </div>
              <div>
                <span style={{ color: '#666', fontSize: '0.85rem' }}>Raw IP Host:</span>{' '}
                <strong style={{ color: result.analysis.is_ip ? '#E63946' : '#171717' }}>
                  {result.analysis.is_ip ? 'Yes ⚠️' : 'No'}
                </strong>
              </div>
              <div>
                <span style={{ color: '#666', fontSize: '0.85rem' }}>Shortened Link:</span>{' '}
                <strong style={{ color: result.analysis.is_shortened ? '#E63946' : '#171717' }}>
                  {result.analysis.is_shortened ? 'Yes ⚠️' : 'No'}
                </strong>
              </div>
              <div>
                <span style={{ color: '#666', fontSize: '0.85rem' }}>Entropy Level:</span>{' '}
                <strong style={{ color: '#171717' }}>{result.analysis.entropy}</strong>
              </div>
            </div>
          </div>

          {/* Indicators Breakdown */}
          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '14px' }}>
            ⚠️ Structural Warning Indicators ({result.analysis.indicator_count})
          </h3>

          {result.analysis.indicators && result.analysis.indicators.length > 0 ? (
            result.analysis.indicators.map((ind, idx) => (
              <div key={idx} className="warning-box">
                <div style={{ color: '#A4161A', fontWeight: 700, fontSize: '1.05rem', marginBottom: '4px' }}>
                  [{ind.severity}] {ind.title}
                </div>
                <div style={{ color: '#4A5568', fontSize: '0.95rem' }}>{ind.details}</div>
              </div>
            ))
          ) : (
            <div className="action-box">
              <div style={{ color: '#15803D', fontWeight: 700 }}>✅ No Suspicious Domain Anomalies Detected</div>
              <div style={{ color: '#374151', fontSize: '0.95rem' }}>
                The hostname structure, protocol, and top-level domain align with normal website standards.
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

          {/* Download Forensic URL Report Button */}
          <div style={{ marginTop: '24px' }}>
            <button className="btn-secondary" onClick={handleDownloadReport} style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
              <Download size={18} />
              Download Forensic URL Threat Report (.txt)
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
