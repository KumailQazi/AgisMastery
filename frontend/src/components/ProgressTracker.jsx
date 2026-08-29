import React from 'react';

export function ProgressTracker({ attempts = 0, successRate = 0, masteryAchieved = false }) {
  const percent = Math.min(100, Math.round(successRate * 100));

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
      <div className="flex justify-between items-center">
        <h4 className="text-sm font-bold text-slate-200 flex items-center gap-2">
          <span>🏆</span> Decision Mastery (4/5 Rule)
        </h4>
        <span
          className={`text-xs px-2.5 py-0.5 rounded-full font-semibold ${
            masteryAchieved
              ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
              : 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30'
          }`}
        >
          {masteryAchieved ? 'Mastery Achieved 🎉' : 'In Progress'}
        </span>
      </div>

      <div className="space-y-1.5">
        <div className="flex justify-between text-xs text-slate-400">
          <span>Accuracy Rate: {percent}%</span>
          <span>{attempts}/5 Completed Attempts</span>
        </div>
        <div className="w-full h-2.5 bg-slate-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-500 transition-all duration-500"
            style={{ width: `${percent}%` }}
          />
        </div>
      </div>
    </div>
  );
}
