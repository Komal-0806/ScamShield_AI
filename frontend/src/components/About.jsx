import React, { useState } from 'react';
import { Phone, Shield, ExternalLink, HelpCircle, Check, X } from 'lucide-react';

export default function About() {
  const [q1Selected, setQ1Selected] = useState(null);
  const [q2Selected, setQ2Selected] = useState(null);

  const bankContacts = [
    { name: 'State Bank of India (SBI)', phone: '1800 1234 / 1800 2100', sms: "SMS 'BLOCK <card_last_4>' to 567676" },
    { name: 'HDFC Bank', phone: '1800 202 6161 / 1800 1600', sms: 'Use MobileBanking app to freeze cards' },
    { name: 'ICICI Bank', phone: '1800 1080', sms: "SMS 'BLOCK <account_number>' to 9215676766" },
    { name: 'Axis Bank', phone: '1860 419 5555 / 1860 500 5555', sms: "SMS 'BLOCK <card_no>' to 56161600" },
    { name: 'Punjab National Bank (PNB)', phone: '1800 1800 / 1800 2021', sms: "SMS 'HOTLIST' to 5607040" }
  ];

  return (
    <div className="container" style={{ paddingTop: '32px', paddingBottom: '60px' }}>
      <div style={{ marginBottom: '28px' }}>
        <h2 style={{ fontSize: '2.0rem', fontWeight: 800, color: '#171717', marginBottom: '6px' }}>
          About <span style={{ color: '#E63946' }}>ScamShield AI</span> & Emergency Resources
        </h2>
        <p style={{ color: '#666666', fontSize: '1.05rem', margin: 0 }}>
          Our mission is to make advanced digital threat awareness accessible, transparent, and actionable for everyone.
        </p>
      </div>

      {/* Emergency Helpline Banner */}
      <div style={{
        background: 'linear-gradient(135deg, #FFF5F5 0%, #FFFFFF 100%)',
        border: '2px solid #E63946',
        borderRadius: '18px',
        padding: '28px',
        marginBottom: '32px'
      }}>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'flex-start' }}>
          <div style={{ fontSize: '2.4rem' }}>🆘</div>
          <div>
            <h3 style={{ fontSize: '1.35rem', fontWeight: 800, color: '#991B1B', marginBottom: '4px' }}>
              National Cyber Crime Emergency Helpline (India)
            </h3>
            <p style={{ color: '#4A5568', fontSize: '1.0rem', marginBottom: '16px' }}>
              If you have fallen victim to financial fraud, act within the critical <strong>Golden Hour</strong> to freeze stolen funds in transit.
            </p>
            <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', alignItems: 'center' }}>
              <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#E63946' }}>
                📞 Dial Toll-Free: 1930
              </div>
              <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#171717' }}>
                🌐 Portal:{' '}
                <a
                  href="https://cybercrime.gov.in"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: '#E63946', textDecoration: 'none' }}
                >
                  cybercrime.gov.in <ExternalLink size={14} style={{ display: 'inline' }} />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bank Hotlines */}
      <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#171717', marginBottom: '16px' }}>
        🏦 Major Bank Emergency Fraud Hotlines
      </h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '14px', marginBottom: '36px' }}>
        {bankContacts.map((b, idx) => (
          <div key={idx} className="card" style={{ padding: '20px' }}>
            <strong style={{ color: '#171717', fontSize: '1.05rem' }}>{b.name}</strong>
            <div style={{ color: '#E63946', fontWeight: 700, marginTop: '4px' }}>📞 {b.phone}</div>
            <div style={{ fontSize: '0.85rem', color: '#666666', marginTop: '4px' }}>{b.sms}</div>
          </div>
        ))}
      </div>

      {/* Privacy Guarantee Card */}
      <div className="card" style={{ borderLeft: '5px solid #E63946', marginBottom: '40px' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#171717', marginBottom: '8px' }}>
          🔒 Zero-Knowledge Privacy Architecture
        </h3>
        <p style={{ color: '#4A5568', fontSize: '0.95rem', lineHeight: 1.6, margin: 0 }}>
          ScamShield AI operates under strict zero-knowledge principles. When you submit a link or message, our heuristic engine parses syntactic attributes in memory. We never store personal identifiers, we never retain confidential passwords or OTPs, and we never ping or execute remote payloads from untrusted links.
        </p>
      </div>

      {/* Interactive Spot-the-Phish Quiz */}
      <h3 style={{ fontSize: '1.35rem', fontWeight: 800, color: '#171717', marginBottom: '14px' }}>
        🧠 Test Your Scam Awareness: Spot the Phish
      </h3>

      <div className="card" style={{ marginBottom: '18px' }}>
        <h4 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '12px' }}>
          Question 1: You receive an urgent SMS: "Your electricity will be cut in 2 hours unless you call 9876543210 to update KYC." What should you do?
        </h4>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {[
            { text: 'Call the number immediately to avoid power loss.', correct: false },
            { text: 'Click any attached link to settle the bill fast.', correct: false },
            { text: 'Do NOT call the number. Check your electricity bill independently and verify on the official board website.', correct: true },
            { text: 'Forward the message to friends to warn them.', correct: false }
          ].map((opt, i) => (
            <button
              key={i}
              className="btn-secondary"
              style={{
                textAlign: 'left',
                backgroundColor: q1Selected === i ? (opt.correct ? '#DCFCE7' : '#FEE2E2') : '#FFFFFF',
                borderColor: q1Selected === i ? (opt.correct ? '#16A34A' : '#DC2626') : '#E5E7EB'
              }}
              onClick={() => setQ1Selected(i)}
            >
              {opt.text}
            </button>
          ))}
        </div>
        {q1Selected !== null && (
          <div style={{ marginTop: '12px', fontWeight: 600, fontSize: '0.92rem', color: q1Selected === 2 ? '#15803D' : '#B91C1C' }}>
            {q1Selected === 2 ? '✅ Correct! Electricity boards never disconnect power within 2 hours via SMS.' : '❌ Incorrect. This is a classic urgency scam! Scammers create fear to force immediate calls.'}
          </div>
        )}
      </div>

      <div className="card">
        <h4 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '12px' }}>
          Question 2: An HR manager on Telegram asks you to like 5 YouTube videos to earn ₹500, but later requires a ₹1,000 "security deposit" for VIP tasks. Is this genuine?
        </h4>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {[
            { text: 'Yes, many multinational tech companies recruit this way.', correct: false },
            { text: 'No, this is a textbook Task / Investment Scam. Legitimate employers never charge advance security deposits.', correct: true },
            { text: 'Yes, as long as they provide an ID card over Telegram.', correct: false }
          ].map((opt, i) => (
            <button
              key={i}
              className="btn-secondary"
              style={{
                textAlign: 'left',
                backgroundColor: q2Selected === i ? (opt.correct ? '#DCFCE7' : '#FEE2E2') : '#FFFFFF',
                borderColor: q2Selected === i ? (opt.correct ? '#16A34A' : '#DC2626') : '#E5E7EB'
              }}
              onClick={() => setQ2Selected(i)}
            >
              {opt.text}
            </button>
          ))}
        </div>
        {q2Selected !== null && (
          <div style={{ marginTop: '12px', fontWeight: 600, fontSize: '0.92rem', color: q2Selected === 1 ? '#15803D' : '#B91C1C' }}>
            {q2Selected === 1 ? '✅ Correct! Legitimate organizations never hire solely via Telegram or demand fees for work.' : '❌ Incorrect. No legitimate employer asks you to deposit money to unlock tasks!'}
          </div>
        )}
      </div>
    </div>
  );
}

