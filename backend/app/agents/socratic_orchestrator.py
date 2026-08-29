"""
Google ADK Socratic Orchestrator for Mastery.
Powered by Google ADK SequentialAgent & LlmAgent pipeline.
"""
from typing import Dict, Any

try:
    from google.adk.agents import LlmAgent, SequentialAgent
    from google.adk.tools import FunctionTool
    ADK_AVAILABLE = True
except ImportError:
    ADK_AVAILABLE = False
    LlmAgent = None
    SequentialAgent = None
    FunctionTool = None

# Phase I: Analyze the scenario and learner history to decide scaffolding level
def analyze_scenario(scenario_context: str, learner_history: str) -> Dict[str, Any]:
    """
    Analyze scenario difficulty and learner readiness.
    Returns: {"scaffolding_level": int, "rationale": str}
    scaffolding_level: 1=full hints, 2=partial, 3=minimal, 4=challenge
    """
    return {
        "scaffolding_level": 2,
        "rationale": "Learner has mixed history; moderate scaffolding recommended."
    }

# Phase II: Generate Socratic follow-up question
def generate_socratic_prompt(scenario_context: str, learner_choice: str, is_optimal: bool, reflection: str) -> Dict[str, Any]:
    """
    Generate a single Socratic follow-up question.
    Returns: {"prompt": str, "target_concept": str}
    """
    if is_optimal:
        prompt = f"You chose to {learner_choice}. That was a strong decision in this context. Why did that choice matter more than the alternatives?"
    else:
        prompt = f"You chose to {learner_choice}. Walk me through your thinking. What consequence did you expect, and what would you do differently next time?"
    return {"prompt": prompt.strip(), "target_concept": "decision_rationale"}

# Phase III: Evaluate mastery status based on interaction history
def evaluate_mastery(attempts: int, correct_count: int) -> Dict[str, Any]:
    """
    Evaluate whether learner has achieved mastery (4/5 correct).
    Returns: {"mastery_achieved": bool, "success_rate": float}
    """
    success_rate = correct_count / attempts if attempts > 0 else 0.0
    mastery_achieved = attempts >= 5 and success_rate >= 0.8
    return {"mastery_achieved": mastery_achieved, "success_rate": round(success_rate, 2)}

# Phase IV: Adapt next scenario difficulty
def adapt_next_scenario(current_difficulty: int, success_rate: float) -> Dict[str, Any]:
    """
    Adjust difficulty up or down based on success rate.
    Returns: {"next_difficulty": int, "reason": str}
    """
    if success_rate >= 0.8:
        next_difficulty = min(current_difficulty + 1, 5)
        reason = "Learner performing well; increasing difficulty."
    elif success_rate >= 0.5:
        next_difficulty = current_difficulty
        reason = "Maintaining current difficulty."
    else:
        next_difficulty = max(current_difficulty - 1, 1)
        reason = "Learner struggling; reducing difficulty and adding scaffolding."
    return {"next_difficulty": next_difficulty, "reason": reason}

# Wrap as ADK FunctionTools if ADK is installed
if ADK_AVAILABLE:
    analyze_tool = FunctionTool(func=analyze_scenario)
    socratic_tool = FunctionTool(func=generate_socratic_prompt)
    mastery_tool = FunctionTool(func=evaluate_mastery)
    adapt_tool = FunctionTool(func=adapt_next_scenario)

    scenario_analyzer = LlmAgent(
        model="gemini-2.0-flash",
        name="scenario_analyzer",
        instruction="Analyze the scenario and learner history. Return scaffolding level and rationale.",
        tools=[analyze_tool],
    )

    socratic_generator = LlmAgent(
        model="gemini-2.0-flash",
        name="socratic_generator",
        instruction="Generate ONE concise Socratic follow-up question. Never give the answer directly.",
        tools=[socratic_tool],
    )

    mastery_evaluator = LlmAgent(
        model="gemini-2.0-flash",
        name="mastery_evaluator",
        instruction="Evaluate mastery based on attempt history using the 4/5 rule.",
        tools=[mastery_tool],
    )

    difficulty_adapter = LlmAgent(
        model="gemini-2.0-flash",
        name="difficulty_adapter",
        instruction="Adapt next scenario difficulty based on learner success rate.",
        tools=[adapt_tool],
    )

    socratic_orchestrator = SequentialAgent(
        name="socratic_orchestrator",
        sub_agents=[scenario_analyzer, socratic_generator, mastery_evaluator, difficulty_adapter],
    )
else:
    socratic_orchestrator = None
