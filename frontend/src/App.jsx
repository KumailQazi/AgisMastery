import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { LearnerPage } from './pages/LearnerPage';
import { CreatorPage } from './pages/CreatorPage';
import { AdminPage } from './pages/AdminPage';

export default function App() {
  const location = useLocation();

  const navLinks = [
    { path: '/', label: 'Learner Scenario', icon: '🎯' },
    { path: '/creator', label: 'Creator Studio', icon: '👩‍🏫' },
    { path: '/admin', label: 'Admin Governance', icon: '🛡️' },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      {/* Navigation Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-2xl bg-gradient-to-r from-indigo-500 to-purple-500 p-2 rounded-xl text-white shadow-lg shadow-indigo-500/30">
            ⚡
          </span>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
              MASTERY <span className="text-xs bg-indigo-500/20 text-indigo-400 px-2 py-0.5 rounded-full border border-indigo-500/30">ADK 2.0</span>
            </h1>
            <p className="text-xs text-slate-400">Socratic Scaffolding & Silent Telemetry Engine</p>
          </div>
        </div>

        <nav className="flex items-center gap-1 bg-slate-800/60 p-1.5 rounded-xl border border-slate-700/60">
          {navLinks.map((link) => {
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all flex items-center gap-2 ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700/40'
                }`}
              >
                <span>{link.icon}</span> {link.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-3">
          <span className="text-xs font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" /> Telemetry Active
          </span>
        </div>
      </header>

      {/* Main View Routes */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full">
        <Routes>
          <Route path="/" element={<LearnerPage />} />
          <Route path="/creator" element={<CreatorPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-4 text-center text-xs text-slate-500">
        Google All Things Agentic Hackathon 2026 | Powered by Gemini 3.5 & Google ADK
      </footer>
    </div>
  );
}
