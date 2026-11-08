import React from 'react';
import { Shield } from 'lucide-react';

export default function Navbar({ activePage, setActivePage }) {
  return (
    <nav className="navbar">
      <div className="container nav-container">
        <div className="nav-brand" onClick={() => setActivePage('home')}>
          <Shield color="#E63946" size={28} strokeWidth={2.5} />
          <div>
            <span>Scam</span><span className="nav-brand-red">Shield</span>
            <span style={{
              marginLeft: '6px',
              fontSize: '0.75rem',
              fontWeight: 800,
              backgroundColor: '#E63946',
              color: '#FFFFFF',
              padding: '2px 7px',
              borderRadius: '6px',
              verticalAlign: 'middle'
            }}>AI</span>
          </div>
        </div>

        <div className="nav-links">
          <button
            className={`nav-btn ${activePage === 'home' ? 'active' : ''}`}
            onClick={() => setActivePage('home')}
          >
            Home
          </button>
          <button
            className={`nav-btn ${activePage === 'messages' ? 'active' : ''}`}
            onClick={() => setActivePage('messages')}
          >
            Message Checker
          </button>
          <button
            className={`nav-btn ${activePage === 'urls' ? 'active' : ''}`}
            onClick={() => setActivePage('urls')}
          >
            URL Checker
          </button>
          <button
            className={`nav-btn ${activePage === 'about' ? 'active' : ''}`}
            onClick={() => setActivePage('about')}
          >
            About & Security
          </button>
          <button
            className={`nav-btn ${activePage === 'history' ? 'active' : ''}`}
            onClick={() => setActivePage('history')}
          >
            Activity Log
          </button>
          <button
            className="btn-primary"
            style={{ marginLeft: '12px' }}
            onClick={() => setActivePage('messages')}
          >
            Get Protected
          </button>
        </div>
      </div>
    </nav>
  );
}

