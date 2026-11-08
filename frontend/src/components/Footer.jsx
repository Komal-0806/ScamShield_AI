import React from 'react';
import { Shield } from 'lucide-react';

export default function Footer({ setActivePage }) {
  return (
    <footer style={{
      borderTop: '1px solid #E5E7EB',
      backgroundColor: '#FFFFFF',
      padding: '48px 0 32px 0',
      marginTop: 'auto'
    }}>
      <div className="container" style={{ textAlign: 'center' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <Shield color="#E63946" size={22} strokeWidth={2.5} />
          <span style={{ fontSize: '1.2rem', fontWeight: 800, color: '#171717' }}>
            Scam<span style={{ color: '#E63946' }}>Shield</span> AI
          </span>
        </div>

        <p style={{ color: '#666666', fontSize: '0.95rem', marginBottom: '20px' }}>
          Think Before You Click. Stay Safe Before You Trust.
        </p>

        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '24px',
          flexWrap: 'wrap',
          fontSize: '0.9rem',
          fontWeight: 600,
          color: '#666666',
          marginBottom: '20px'
        }}>
          <span style={{ cursor: 'pointer' }} onClick={() => setActivePage('home')}>Home</span>
          <span>•</span>
          <span style={{ cursor: 'pointer' }} onClick={() => setActivePage('messages')}>Message Checker</span>
          <span>•</span>
          <span style={{ cursor: 'pointer' }} onClick={() => setActivePage('urls')}>URL Checker</span>
          <span>•</span>
          <span style={{ cursor: 'pointer' }} onClick={() => setActivePage('about')}>Emergency Helplines</span>
          <span>•</span>
          <a
            href="https://cybercrime.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#E63946', textDecoration: 'none' }}
          >
            National Cyber Crime Portal (1930)
          </a>
        </div>

        <div style={{ color: '#9CA3AF', fontSize: '0.82rem' }}>
          © {new Date().getFullYear()} ScamShield AI Platform. Designed with zero-knowledge, privacy-first principles.
        </div>
      </div>
    </footer>
  );
}
