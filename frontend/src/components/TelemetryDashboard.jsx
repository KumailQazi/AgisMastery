import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts';

export function TelemetryDashboard({ data }) {
  const chartData = [
    { name: 'Completion', rate: 94.2, fill: '#10b981' },
    { name: 'Mastery', rate: 58.4, fill: '#ef4444' },
  ];

  const struggleData = [
    { name: 'Scenario #1', struggleIndex: 42, avgTime: 14.8 },
    { name: 'Scenario #2', struggleIndex: 78, avgTime: 32.4 },
    { name: 'Scenario #3', struggleIndex: 24, avgTime: 11.2 },
  ];

  return (
    <div className="space-y-6">
      {/* Top Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
          <span className="text-xs text-slate-400 font-semibold">Course Completion</span>
          <div className="text-3xl font-extrabold text-emerald-400 mt-1">94.2%</div>
          <span className="text-xs text-slate-500">Traditional slide metrics</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
          <span className="text-xs text-slate-400 font-semibold">Actual Decision Mastery</span>
          <div className="text-3xl font-extrabold text-rose-400 mt-1">58.4%</div>
          <span className="text-xs text-slate-500">Passed 4/5 high-stakes branches</span>
        </div>

        <div className="bg-slate-900 border border-amber-500/30 bg-amber-500/5 rounded-2xl p-5 shadow-xl">
          <span className="text-xs text-amber-300 font-semibold">The Mastery Gap</span>
          <div className="text-3xl font-extrabold text-amber-400 mt-1">35.8%</div>
          <span className="text-xs text-slate-500">Finished course without mastery</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
          <span className="text-xs text-slate-400 font-semibold">Socratic Recovery</span>
          <div className="text-3xl font-extrabold text-indigo-400 mt-1">+37.0%</div>
          <span className="text-xs text-slate-500">Accuracy gain on 2nd attempt</span>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
          <h3 className="text-sm font-bold text-slate-200 mb-4 flex items-center gap-2">
            <span>📉</span> Completion vs. Mastery Gap
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" domain={[0, 100]} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                <Bar dataKey="rate" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
          <h3 className="text-sm font-bold text-slate-200 mb-4 flex items-center gap-2">
            <span>🔥</span> Cognitive Load & Struggle Heatmap
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={struggleData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" domain={[0, 100]} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                <Line type="monotone" dataKey="struggleIndex" stroke="#ef4444" strokeWidth={3} dot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
