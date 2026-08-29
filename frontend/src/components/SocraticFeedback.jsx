import React from 'react';

export function SocraticFeedback({ consequence, socraticPrompt, isOptimal }) {
  if (!consequence && !socraticPrompt) return null;

  return (
    <div className="bg-slate-900/90 border border-indigo-500/40 rounded-2xl p-6 shadow-xl space-y-4">
      <div className="flex items-center gap-3 border-b border-slate-800 pb-3">
        <span className="text-2xl">🤖</span>
        <div>
          <h3 className="text-base font-bold text-indigo-300">Gemini Socratic Agent Feedback</h3>
          <p className="text-xs text-slate-400">SequentialAgent Scaffolding Evaluation</p>
        </div>
      </div>

      <div className="space-y-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          Downstream Consequence
        </span>
        <p className="text-sm text-slate-200 bg-slate-800/60 p-3.5 rounded-xl border border-slate-700/60">
          {consequence}
        </p>
      </div>

      <div className="space-y-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400">
          Socratic Follow-Up Reflection Prompt
        </span>
        <div className="p-4 bg-indigo-950/50 rounded-xl border border-indigo-500/30 text-indigo-200 text-sm italic font-serif">
          "{socraticPrompt}"
        </div>
      </div>
    </div>
  );
}
