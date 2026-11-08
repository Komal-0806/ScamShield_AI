import React from 'react';
import { ShieldCheck, MessageSquare, Link, Zap, Lock, Eye, AlertTriangle } from 'lucide-react';

export default function Hero({ setActivePage }) {
  return (
    <div className="container" style={{ paddingTop: '32px', paddingBottom: '60px' }}>
      {/* Hero Banner */}
      <div style={{
        background: 'linear-gradient(180deg, #FFFFFF 0%, #FFF5F5 100%)',
        border: '1px solid #FFE4E6',
        borderRadius: '24px',
        padding: '52px 36px',
        textAlign: 'center',
        marginBottom: '40px',
        boxShadow: '0 10px 30px rgba(230, 57, 70, 0.05)'
      }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          backgroundColor: '#FFE5E7',
          color: '#A4161A',
          fontSize: '0.85rem',
          fontWeight: 700,
          padding: '6px 16px',
          borderRadius: '999px',
          marginBottom: '20px',
          border: '1px solid #FFCCD0'
        }}>
          <span style={{ width: '8px', height: '8px', backgroundColor: '#E63946', borderRadius: '50%' }}></span>
          Intelligent Digital Safety Platform
        </div>

        <h1 style={{
          fontSize: '3.0rem',
          fontWeight: 800,
          lineHeight: 1.15,
          color: '#171717',
          marginBottom: '16px',
          letterSpacing: '-0.02em'
        }}>
          Your Digital Safety <span style={{ color: '#E63946' }}>Starts Here.</span>
        </h1>

        <p style={{
          fontSize: '1.15rem',
          color: '#666666',
          maxWidth: '740px',
          margin: '0 auto 32px auto',
          lineHeight: 1.6
        }}>
          ScamShield AI proactively protects everyday users from deceptive SMS messages, fraudulent WhatsApp job offers, payment traps, and brand-impersonating links before you trust them.
        </p>

        {/* Action Callout Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '20px',
          maxWidth: '850px',
          margin: '0 auto',
          textAlign: 'left'
        }}>
          <div className="card" style={{ borderTop: '4px solid #E63946' }}>
            <div style={{ fontSize: '1.8rem', marginBottom: '10px' }}>💬</div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '6px' }}>Message & Job Offer Checker</h3>
            <p style={{ color: '#666666', fontSize: '0.92rem', marginBottom: '16px' }}>
              Received a suspicious text, part-time task pitch, or urgent bill notice? Paste it here to uncover red flags.
            </p>
            <button
              className="btn-primary"
              style={{ width: '100%', justifyContent: 'center' }}
              onClick={() => setActivePage('messages')}
            >
              Check a Message Now
            </button>
          </div>

          <div className="card" style={{ borderTop: '4px solid #A4161A' }}>
            <div style={{ fontSize: '1.8rem', marginBottom: '10px' }}>🔗</div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '6px' }}>Suspicious URL Inspector</h3>
            <p style={{ color: '#666666', fontSize: '0.92rem', marginBottom: '16px' }}>
              Unsure about a link? We inspect domain structures, typosquatting, and brand spoofing without opening it.
            </p>
            <button
              className="btn-secondary"
              style={{ width: '100%', justifyContent: 'center' }}
              onClick={() => setActivePage('urls')}
            >
              Inspect a Link Safely
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: '16px',
        marginBottom: '60px'
      }}>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#E63946' }}>1,500+</div>
          <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#666666', textTransform: 'uppercase' }}>Inquiries Verified</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#A4161A' }}>420+</div>
          <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#666666', textTransform: 'uppercase' }}>High-Risk Threats Flagged</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#16A34A' }}>&lt; 0.8s</div>
          <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#666666', textTransform: 'uppercase' }}>Instant Analysis Speed</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#171717' }}>100%</div>
          <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#666666', textTransform: 'uppercase' }}>Zero-Knowledge Privacy</div>
        </div>
      </div>

      {/* 3 Step Process */}
      <div style={{ textAlign: 'center', marginBottom: '50px' }}>
        <div style={{ color: '#E63946', fontWeight: 700, fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>How It Works</div>
        <h2 style={{ fontSize: '2.0rem', fontWeight: 800, margin: '8px 0 12px 0' }}>Three Steps to Absolute Clarity</h2>
        <p style={{ color: '#666666', maxWidth: '600px', margin: '0 auto 36px auto' }}>
          ScamShield eliminates the guesswork behind deceptive digital interactions.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', textAlign: 'left' }}>
          <div className="card">
            <div style={{ width: '36px', height: '36px', borderRadius: '10px', backgroundColor: '#FFF5F5', color: '#E63946', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, marginBottom: '16px' }}>1</div>
            <h4 style={{ fontWeight: 700, fontSize: '1.15rem', marginBottom: '8px' }}>Paste Suspicious Input</h4>
            <p style={{ color: '#666666', fontSize: '0.92rem' }}>
              Submit any SMS, WhatsApp forward, part-time job message, or link into our secure console.
            </p>
          </div>
          <div className="card">
            <div style={{ width: '36px', height: '36px', borderRadius: '10px', backgroundColor: '#FFF5F5', color: '#E63946', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, marginBottom: '16px' }}>2</div>
            <h4 style={{ fontWeight: 700, fontSize: '1.15rem', marginBottom: '8px' }}>Intelligent Threat Engine</h4>
            <p style={{ color: '#666666', fontSize: '0.92rem' }}>
              Our dual-layer engine inspects social engineering panic cues, credential demands, and domain typosquatting.
            </p>
          </div>
          <div className="card">
            <div style={{ width: '36px', height: '36px', borderRadius: '10px', backgroundColor: '#FFF5F5', color: '#E63946', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, marginBottom: '16px' }}>3</div>
            <h4 style={{ fontWeight: 700, fontSize: '1.15rem', marginBottom: '8px' }}>Actionable Guidance</h4>
            <p style={{ color: '#666666', fontSize: '0.92rem' }}>
              Receive an explainable risk rating, specific red flags highlighted, and prioritized safety recommendations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

