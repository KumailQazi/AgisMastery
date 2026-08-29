import React, { useState } from 'react';
import { TelemetryDashboard } from '../components/TelemetryDashboard';
import { ScenarioBuilder } from '../components/ScenarioBuilder';

export function CreatorPage() {
  const [activeTab, setActiveTab] = useState('analytics');

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-white">Course Creator Studio & Telemetry Analytics</h2>
          <p className="text-xs text-slate-400">Inspect struggle heatmaps and design adaptive decision scenarios</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setActiveTab('analytics')}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'analytics'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            📊 Telemetry Dashboard
          </button>
          <button
            onClick={() => setActiveTab('builder')}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'builder'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            🛠️ Scenario Builder
          </button>
        </div>
      </div>

      {activeTab === 'analytics' ? <TelemetryDashboard /> : <ScenarioBuilder />}
    </div>
  );
}
