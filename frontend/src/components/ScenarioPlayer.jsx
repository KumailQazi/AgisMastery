import React, { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

export function ScenarioPlayer({ scenario, learnerId = 1 }) {
  const [selectedBranch, setSelectedBranch] = useState(null);
  const [reflectionText, setReflectionText] = useState('');
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [apiResult, setApiResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const sessionId = `session-learner-${learnerId}-scenario-${scenario?.scenario_id || 1}`;
  const {
    isConnected,
    socraticPrompt,
    flowState,
    reflectionFeedback,
    sendDecision,
    sendCognitiveLoad,
    sendReflection,
  } = useWebSocket(sessionId);

  // Hesitation & Cognitive load tracker (every 10s)
  useEffect(() => {
    const timer = setInterval(() => {
      setElapsedSeconds((prev) => {
        const next = prev + 1;
        if (next % 10 === 0 && !selectedBranch) {
          sendCognitiveLoad({
            hesitation_seconds: next,
            scenario_id: scenario?.scenario_id,
            learner_id: learnerId,
          });
        }
        return next;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [selectedBranch, scenario, learnerId, sendCognitiveLoad]);

  const handleBranchClick = (branch) => {
    setSelectedBranch(branch);
  };

  const handleDecisionSubmit = async () => {
    if (!selectedBranch) return;
    setIsSubmitting(true);

    const payload = {
      learner_id: learnerId,
      branch_id: selectedBranch.branch_id,
      scenario_id: scenario?.scenario_id,
      is_optimal: selectedBranch.is_optimal,
      time_spent_seconds: elapsedSeconds,
    };

    // 1. Send via WebSocket for instant live Socratic feedback
    sendDecision(payload);

    // 2. Persist via REST API for DB persistence
    try {
      const res = await fetch(`http://localhost:8000/api/scenarios/${scenario?.scenario_id}/decide`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        const data = await res.json();
        setApiResult(data);
      }
    } catch (err) {
      console.warn('REST API unavailable; relying on WebSocket relay', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReflectionSubmit = (e) => {
    e.preventDefault();
    if (!reflectionText.trim()) return;

    sendReflection({
      learner_id: learnerId,
      scenario_id: scenario?.scenario_id,
      reflection_text: reflectionText,
    });
  };

  return (
    <div className="bg-slate-900 text-slate-100 rounded-2xl p-6 shadow-2xl border border-slate-800 max-w-4xl mx-auto">
      {/* Header with Connection & Cognitive Load Badges */}
      <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-4">
        <div>
          <span className="text-xs uppercase tracking-wider text-indigo-400 font-semibold">
            Scenario #{scenario?.scenario_id || 1}
          </span>
          <h2 className="text-xl font-bold text-white mt-1">
            {scenario?.decision_point || 'The 10-Minute Launch Override'}
          </h2>
        </div>
        <div className="flex items-center gap-3">
          {/* Cognitive Load Banner */}
          {flowState && (
            <span
              className={`text-xs px-3 py-1 rounded-full font-medium ${
                flowState.suggest_scaffolding
                  ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                  : 'bg-sky-500/20 text-sky-300 border border-sky-500/40'
              }`}
            >
              Signal: {flowState.signal}
            </span>
          )}

          {/* WebSocket Connection Status */}
          <span
            className={`text-xs px-2.5 py-1 rounded-full flex items-center gap-1.5 ${
              isConnected
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full ${
                isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'
              }`}
            />
            {isConnected ? 'Relay Live' : 'Reconnecting...'}
          </span>
        </div>
      </div>

      {/* Scenario Context */}
      <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/60 mb-6">
        <p className="text-slate-300 text-sm leading-relaxed">
          {scenario?.context ||
            'You are 10 minutes before launch. The client VP demands an immediate security override. Bypassing protocol ensures an on-time kickoff but violates security.'}
        </p>
      </div>

      {/* Decision Branches */}
      <div className="space-y-3 mb-6">
        <h3 className="text-sm font-semibold text-slate-400">Select Decision Path:</h3>
        {(scenario?.branches || [
          { branch_id: 1, choice_text: 'Approve the override immediately for the press launch.', is_optimal: false },
          { branch_id: 2, choice_text: 'Refuse the override and escalate to the Incident Commander.', is_optimal: true },
          { branch_id: 3, choice_text: 'Quietly run partial checks without full disclosure.', is_optimal: false },
        ]).map((branch) => (
          <div
            key={branch.branch_id}
            onClick={() => handleBranchClick(branch)}
            className={`p-4 rounded-xl border cursor-pointer transition-all duration-200 ${
              selectedBranch?.branch_id === branch.branch_id
                ? 'bg-indigo-950/60 border-indigo-500 shadow-lg shadow-indigo-500/20'
                : 'bg-slate-800/40 border-slate-700/60 hover:bg-slate-800 hover:border-slate-600'
            }`}
          >
            <p className="text-sm font-medium text-slate-200">{branch.choice_text}</p>
          </div>
        ))}
      </div>

      <button
        onClick={handleDecisionSubmit}
        disabled={!selectedBranch || isSubmitting}
        className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50 text-white font-semibold shadow-lg shadow-indigo-500/30 transition-all mb-6"
      >
        {isSubmitting ? 'Evaluating Socratic Loop...' : 'Commit Decision & Stream Feedback →'}
      </button>

      {/* Real-time Socratic Agent Prompt (Via WebSocket / API) */}
      {(socraticPrompt || apiResult) && (
        <div className="bg-indigo-950/40 border border-indigo-500/40 rounded-xl p-5 mb-6 animate-fade-in">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">🤖</span>
            <h4 className="text-sm font-bold text-indigo-300">Gemini Socratic Agent</h4>
          </div>
          <p className="text-xs text-slate-400 mb-2">
            <strong>Consequence:</strong>{' '}
            {socraticPrompt?.consequence || apiResult?.consequence}
          </p>
          <div className="p-3 bg-slate-900/80 rounded-lg border border-indigo-500/30 text-indigo-200 text-sm italic">
            "{socraticPrompt?.prompt || apiResult?.socratic_prompt}"
          </div>

          {/* Socratic Reflection Box */}
          <form onSubmit={handleReflectionSubmit} className="mt-4">
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Your Socratic Reflection:
            </label>
            <textarea
              rows="3"
              value={reflectionText}
              onChange={(e) => setReflectionText(e.target.value)}
              placeholder="Explain the mental model and trade-offs behind your choice..."
              className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
            />
            <button
              type="submit"
              className="mt-2 text-xs font-semibold py-2 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-all"
            >
              Submit Reflection
            </button>
          </form>

          {reflectionFeedback && (
            <div className="mt-3 p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-lg text-xs text-emerald-300">
              ✅ {reflectionFeedback}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
