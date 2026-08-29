import React, { useState, useEffect } from 'react';
import { ScenarioPlayer } from '../components/ScenarioPlayer';
import { ProgressTracker } from '../components/ProgressTracker';

export function LearnerPage() {
  const [scenario, setScenario] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/scenarios/1')
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) setScenario(data);
      })
      .catch(() => {});
  }, []);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2">
        <ScenarioPlayer scenario={scenario} learnerId={1} />
      </div>
      <div className="space-y-6">
        <ProgressTracker attempts={1} successRate={1.0} masteryAchieved={false} />
        
        {/* Socratic Scaffolding Guide Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
          <h4 className="text-sm font-bold text-slate-200 flex items-center gap-2">
            <span>💡</span> Socratic Scaffolding Rules
          </h4>
          <ul className="text-xs text-slate-400 space-y-2 leading-relaxed">
            <li>• AI will not give direct answers—it probes your decision rationale.</li>
            <li>• Time pressure & hesitation signals are captured silently to adjust hints.</li>
            <li>• Achieve 4 out of 5 accurate decisions under realistic variations to earn Mastery.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
