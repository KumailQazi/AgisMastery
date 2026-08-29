import React, { useState } from 'react';

export function ScenarioBuilder() {
  const [context, setContext] = useState('');
  const [decisionPoint, setDecisionPoint] = useState('');
  const [branches, setBranches] = useState([
    { choice_text: '', consequence: '', is_optimal: true },
    { choice_text: '', consequence: '', is_optimal: false },
  ]);
  const [saved, setSaved] = useState(false);

  const addBranch = () => {
    setBranches([...branches, { choice_text: '', consequence: '', is_optimal: false }]);
  };

  const handleBranchChange = (index, field, value) => {
    const next = [...branches];
    next[index][field] = value;
    setBranches(next);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <span>🛠️</span> Scenario Studio & Decision Branch Builder
        </h2>
        <p className="text-xs text-slate-400">Design high-stakes decision points with Socratic reflection consequences</p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-300 mb-1">Scenario Workplace Context:</label>
          <textarea
            rows="3"
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="e.g. 10 minutes before launch, customer VP requests a security check override..."
            className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none"
            required
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 mb-1">Critical Decision Point Question:</label>
          <input
            type="text"
            value={decisionPoint}
            onChange={(e) => setDecisionPoint(e.target.value)}
            placeholder="e.g. How do you respond to the emergency escalation?"
            className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none"
            required
          />
        </div>

        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <label className="text-xs font-semibold text-slate-300">Decision Branches & Consequence Paths:</label>
            <button
              type="button"
              onClick={addBranch}
              className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold"
            >
              + Add Branch
            </button>
          </div>

          {branches.map((branch, idx) => (
            <div key={idx} className="p-4 bg-slate-800/60 rounded-xl border border-slate-700 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400">Branch #{idx + 1}</span>
                <label className="flex items-center gap-2 text-xs text-emerald-400 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={branch.is_optimal}
                    onChange={(e) => handleBranchChange(idx, 'is_optimal', e.target.checked)}
                    className="rounded bg-slate-900 border-slate-700 text-indigo-600"
                  />
                  Optimal Choice
                </label>
              </div>

              <input
                type="text"
                value={branch.choice_text}
                onChange={(e) => handleBranchChange(idx, 'choice_text', e.target.value)}
                placeholder="Learner choice option text..."
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
                required
              />

              <textarea
                rows="2"
                value={branch.consequence}
                onChange={(e) => handleBranchChange(idx, 'consequence', e.target.value)}
                placeholder="Realistic downstream consequence..."
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
                required
              />
            </div>
          ))}
        </div>
      </div>

      <button
        type="submit"
        className="w-full py-3 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 text-white font-semibold rounded-xl shadow-lg shadow-indigo-500/20"
      >
        Publish Scenario to Course
      </button>

      {saved && (
        <div className="p-3 bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 rounded-xl text-center text-xs font-semibold">
          ✅ Scenario successfully published and indexed!
        </div>
      )}
    </form>
  );
}
