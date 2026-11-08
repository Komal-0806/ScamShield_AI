import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import MessageChecker from './components/MessageChecker';
import UrlChecker from './components/UrlChecker';
import About from './components/About';
import History from './components/History';
import Footer from './components/Footer';

export default function App() {
  const [activePage, setActivePage] = useState('home');

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [activePage]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar activePage={activePage} setActivePage={setActivePage} />

      <main style={{ flex: 1 }}>
        {activePage === 'home' && <Hero setActivePage={setActivePage} />}
        {activePage === 'messages' && <MessageChecker />}
        {activePage === 'urls' && <UrlChecker />}
        {activePage === 'about' && <About />}
        {activePage === 'history' && <History />}
      </main>

      <Footer setActivePage={setActivePage} />
    </div>
  );
}
