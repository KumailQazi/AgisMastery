import React from 'react';

export function AdminPage() {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-white">Enterprise Governance & Zero-Trust Administration</h2>
        <p className="text-xs text-slate-400">Manage Model Armor PII policies, Cloud Run replicas, and telemetry compliance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
          <div className="flex items-center gap-2">
            <span className="text-xl">🛡️</span>
            <h4 className="text-sm font-bold text-white">Google Model Armor</h4>
          </div>
          <p className="text-xs text-slate-400">
            Active inspection template: <code className="text-indigo-400">mastery-pii-template</code>
          </p>
          <span className="inline-block text-xs bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-2.5 py-0.5 rounded-full font-semibold">
            Status: Active & Redacting PII
          </span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
          <div className="flex items-center gap-2">
            <span className="text-xl">🧠</span>
            <h4 className="text-sm font-bold text-white">Google ADK Agent Fleet</h4>
          </div>
          <p className="text-xs text-slate-400">
            SequentialAgent Pipeline: <code className="text-indigo-400">socratic_orchestrator</code>
          </p>
          <span className="inline-block text-xs bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 px-2.5 py-0.5 rounded-full font-semibold">
            Engine: Gemini 3.5 / 2.0 Flash
          </span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
          <div className="flex items-center gap-2">
            <span className="text-xl">☁️</span>
            <h4 className="text-sm font-bold text-white">Cloud Run & Firestore</h4>
          </div>
          <p className="text-xs text-slate-400">
            Region: <code className="text-indigo-400">us-central1</code> | Ingress: Managed HTTPS
          </p>
          <span className="inline-block text-xs bg-sky-500/20 text-sky-400 border border-sky-500/30 px-2.5 py-0.5 rounded-full font-semibold">
            Health: Healthy (0 Errors)
          </span>
        </div>
      </div>
    </div>
  );
}
