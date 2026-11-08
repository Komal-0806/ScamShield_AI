import React, { useState, useEffect } from 'react';
import { Download, Trash2, RefreshCw } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || '';

export default function History() {
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({ total_scans: 0, high_risk: 0, moderate_risk: 0, low_risk: 0 });
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/history?limit=100`);
      if (res.ok) {
        const data = await res.json();
        setHistory(data.history || []);
        setStats(data.stats || { total_scans: 0, high_risk: 0, moderate_risk: 0, low_risk: 0 });
      }
    } catch (err) {
      console.error('Failed to load history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleClearHistory = async () => {
    if (!window.confirm('Are you sure you want to clear your local scan history?')) return;
    try {
      const res = await fetch(`${API_BASE}/api/history`, { method: 'DELETE' });
      if (res.ok) {
        setHistory([]);
        setStats({ total_scans: 0, high_risk: 0, moderate_risk: 0, low_risk: 0 });
      }
    } catch (err) {
      console.error('Failed to clear history:', err);
    }
  };

  const handleExportCsv = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/history/export`);
      if (res.ok) {
        const data = await res.json();
        const blob = new Blob([data.csv || ''], { type: 'text/csv;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `scamshield_history_${Date.now()}.csv`;
        link.click();
        URL.revokeObjectURL(url);
      }
    } catch (err) {
      console.error('Failed to export CSV:', err);
    }
  };

  return (
    <div className="container" style={{ paddingTop: '32px', paddingBottom: '60px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '2.0rem', fontWeight: 800, color: '#171717', marginBottom: '6px' }}>
          Activity Log & <span style={{ color: '#E63946' }}>Scan History</span>
        </h2>
        <p style={{ color: '#666666', fontSize: '1.05rem', margin: 0 }}>
          Review recent threat inquiries analyzed by ScamShield on this device.
        </p>
      </div>

      {/* Summary Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '14px', marginBottom: '28px' }}>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2.0rem', fontWeight: 800, color: '#171717' }}>{stats.total_scans}</div>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#666666', textTransform: 'uppercase' }}>Total Inquiries Logged</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2.0rem', fontWeight: 800, color: '#E63946' }}>{stats.high_risk}</div>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#666666', textTransform: 'uppercase' }}>High-Risk Threats</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2.0rem', fontWeight: 800, color: '#D97706' }}>{stats.moderate_risk}</div>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#666666', textTransform: 'uppercase' }}>Suspicious Alerts</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2.0rem', fontWeight: 800, color: '#16A34A' }}>{stats.low_risk}</div>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#666666', textTransform: 'uppercase' }}>Safe Checks</div>
        </div>
      </div>

      {/* Table Card */}
      <div className="card" style={{ padding: '0', overflow: 'hidden', marginBottom: '20px' }}>
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: '#666666' }}>
            <RefreshCw className="animate-spin" size={24} style={{ margin: '0 auto 8px auto' }} />
            Loading scan history...
          </div>
        ) : history.length === 0 ? (
          <div style={{ padding: '48px', textAlign: 'center', color: '#666666' }}>
            <div style={{ fontSize: '2.2rem', marginBottom: '8px' }}>📭</div>
            <div style={{ fontWeight: 700, fontSize: '1.1rem', color: '#171717' }}>No Scan Records Found</div>
            <p style={{ fontSize: '0.9rem', marginTop: '4px' }}>Analyze a message or URL to populate this log.</p>
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ backgroundColor: '#F8FAFC', borderBottom: '1px solid #E2E8F0', color: '#475569', fontWeight: 700 }}>
                  <th style={{ padding: '14px 18px' }}>Timestamp</th>
                  <th style={{ padding: '14px 18px' }}>Type</th>
                  <th style={{ padding: '14px 18px' }}>Content Snippet</th>
                  <th style={{ padding: '14px 18px' }}>Risk Score</th>
                  <th style={{ padding: '14px 18px' }}>Verdict</th>
                </tr>
              </thead>
              <tbody>
                {history.map((row) => (
                  <tr key={row.id} style={{ borderBottom: '1px solid #F1F5F9' }}>
                    <td style={{ padding: '14px 18px', color: '#64748B', whiteSpace: 'nowrap' }}>{row.timestamp}</td>
                    <td style={{ padding: '14px 18px', fontWeight: 600 }}>{row.scan_type}</td>
                    <td style={{ padding: '14px 18px', color: '#334155', maxWidth: '350px' }}>{row.content_snippet}</td>
                    <td style={{ padding: '14px 18px', fontWeight: 700, color: row.risk_score >= 60 ? '#DC2626' : row.risk_score >= 30 ? '#D97706' : '#16A34A' }}>
                      {row.risk_score}%
                    </td>
                    <td style={{ padding: '14px 18px' }}>
                      <span className={row.risk_level === 'High Risk' ? 'badge-high' : row.risk_level === 'Moderate Risk' ? 'badge-medium' : 'badge-low'}>
                        {row.verdict}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div style={{ display: 'flex', gap: '12px' }}>
        <button className="btn-secondary" onClick={handleExportCsv} style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
          <Download size={16} /> Export CSV Log
        </button>
        <button className="btn-secondary" onClick={handleClearHistory} style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', color: '#DC2626' }}>
          <Trash2 size={16} /> Clear History
        </button>
      </div>
    </div>
  );
}
