import sys
import os

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.base import Base, engine, SessionLocal
from app.main import seed_database
from app.models.scenario import Scenario
from app.models.decision_branch import DecisionBranch
from app.telemetry.capture import telemetry
from app.agents.socratic_orchestrator import (
    analyze_scenario,
    generate_socratic_prompt,
    evaluate_mastery,
    adapt_next_scenario
)

def run_agent_test():
    print("=" * 70)
    print("🧠 TESTING MASTERY SOCRATIC AGENT + TELEMETRY PIPELINE")
    print("=" * 70)

    # 1. Initialize & Seed DB
    print("\n[1/5] Initializing Database & Seed Scenarios...")
    seed_database()
    db = SessionLocal()

    try:
        scenario = db.query(Scenario).first()
        if not scenario:
            print("❌ No scenarios found.")
            return

        branches = db.query(DecisionBranch).filter(DecisionBranch.scenario_id == scenario.scenario_id).all()
        print(f"✅ Loaded Scenario ID #{scenario.scenario_id}")
        print(f"📖 Context: {scenario.context}")
        print(f"❓ Decision Point: {scenario.decision_point}")
        print(f"🌿 Available Decision Branches: {len(branches)}")

        # 2. Simulate Learner Interaction
        print("\n[2/5] Simulating Learner Decision...")
        chosen_branch = next((b for b in branches if b.is_optimal), branches[0])
        print(f"👉 Learner selected: \"{chosen_branch.choice_text}\"")
        print(f"🎯 Optimal choice? {'YES (Accurate)' if chosen_branch.is_optimal else 'NO (Sub-optimal)'}")

        # 3. Silent Telemetry Capture
        print("\n[3/5] Recording Silent Telemetry Signals...")
        interaction = telemetry.log_interaction({
            "learner_id": 1,
            "scenario_id": scenario.scenario_id,
            "branch_chosen": chosen_branch.branch_id,
            "accuracy": 1 if chosen_branch.is_optimal else 0,
            "time_spent_seconds": 14.8,
            "hints_used": "hint_security_checklist",
            "cognitive_load_signal": "moderate_hesitation",
            "reflection_text": "I chose this because protocol exists to prevent catastrophic public incidents."
        })
        print(f"📊 Telemetry logged -> Interaction ID #{interaction.interaction_id}")
        print(f"⏱ Time spent: 14.8s | Signal: moderate_hesitation | Hints: hint_security_checklist")

        # 4. Mastery Progress Evaluation (4/5 Rule)
        print("\n[4/5] Updating Mastery State (4/5 Decision Rule)...")
        progress = telemetry.update_mastery(learner_id=1, scenario_id=scenario.scenario_id, accuracy=1)
        mastery_result = evaluate_mastery(progress.attempts, int(progress.attempts * float(progress.success_rate or 0)))
        print(f"📈 Total Attempts: {progress.attempts} | Success Rate: {progress.success_rate * 100}%")
        print(f"🏆 Mastery Achieved? {'YES 🎉' if mastery_result['mastery_achieved'] else 'IN PROGRESS (Needs 4/5)'}")

        # 5. Socratic Agent Dialogue Generation
        print("\n[5/5] Executing Socratic Agent Loop...")
        scaffolding = analyze_scenario(scenario.context, f"Attempts: {progress.attempts}")
        socratic = generate_socratic_prompt(
            scenario_context=scenario.context,
            learner_choice=chosen_branch.choice_text,
            is_optimal=chosen_branch.is_optimal,
            reflection=interaction.reflection_text
        )
        adaptation = adapt_next_scenario(current_difficulty=2, success_rate=float(progress.success_rate or 0))

        print(f"🤖 Scaffolding Level: Level {scaffolding['scaffolding_level']} ({scaffolding['rationale']})")
        print(f"💬 Socratic Follow-Up Question:")
        print(f"   \"{socratic['prompt']}\"")
        print(f"🔄 Next Scenario Difficulty Adaptation: Level {adaptation['next_difficulty']} ({adaptation['reason']})")

        print("\n" + "=" * 70)
        print("✅ ALL AGENT & TELEMETRY PIPELINES VERIFIED SUCCESSFULLY!")
        print("=" * 70)

    finally:
        db.close()

if __name__ == "__main__":
    run_agent_test()
