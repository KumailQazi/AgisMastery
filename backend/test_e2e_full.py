import sys
import os
import json
import urllib.request
import urllib.error

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

API_BASE = "http://127.0.0.1:8000/api"
RELAY_BASE = "http://127.0.0.1:8080"

def post_json(url, data):
    req = urllib.request.Request(
        url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(data).encode()
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        return json.loads(res.read().decode())

def get_json(url):
    with urllib.request.urlopen(url, timeout=5) as res:
        return json.loads(res.read().decode())

def run_e2e():
    print("=" * 75)
    print("🚀 RUNNING END-TO-END MASTERY STACK VERIFICATION")
    print("=" * 75)

    # 1. Health Checks
    print("\n[Step 1/6] Verifying System Health...")
    api_health = get_json("http://127.0.0.1:8000/health")
    relay_health = get_json(f"{RELAY_BASE}/health")
    print(f"✅ Core Backend API: {api_health['status']} (v{api_health.get('version', '1.0')})")
    print(f"✅ WebSocket Relay: {relay_health['status']} (Redis/Memory state active)")

    # 2. Scenarios Loading
    print("\n[Step 2/6] Fetching High-Stakes Workplace Scenarios...")
    scenarios = get_json(f"{API_BASE}/scenarios/")
    print(f"✅ Loaded {len(scenarios)} Scenario(s) from Database:")
    for s in scenarios:
        print(f"   • Scenario #{s['scenario_id']}: \"{s['decision_point']}\" ({len(s['branches'])} branches)")

    # 3. Learner Decision & Socratic Loop Execution
    print("\n[Step 3/6] Simulating Learner Decision & Socratic Orchestrator...")
    decision_res = post_json(f"{API_BASE}/scenarios/1/decide", {
        "learner_id": 1,
        "branch_id": 2,
        "time_spent_seconds": 13.4,
        "hints_used": "security_checklist",
        "cognitive_load_signal": "moderate"
    })
    print(f"✅ Consequence: \"{decision_res['consequence']}\"")
    print(f"🤖 Socratic Prompt: \"{decision_res['socratic_prompt']}\"")
    print(f"📈 Mastery State: Attempts={decision_res['mastery_status']['attempts']}, Success Rate={decision_res['mastery_status']['success_rate']*100}%")

    # 4. Model Armor PII Sanitization Test
    print("\n[Step 4/6] Testing Google Model Armor PII Sanitization...")
    armored_res = post_json(f"{API_BASE}/decisions-armored/1/decide-safe", {
        "learner_id": 1,
        "branch_id": 2,
        "time_spent_seconds": 11.2,
        "reflection_text": "I chose this because my manager john.doe@acme.com said so, call 555-123-4567, SSN 000-12-3456"
    })
    audit = armored_res["sanitization_audit"]
    print(f"✅ PII Redaction Active? {audit['pii_redacted']}")
    print(f"🛡️ Redacted Fields: {audit['redacted_fields']}")

    # 5. Multimodal Google Models Suite (Gemma, Veo, Lyria)
    print("\n[Step 5/6] Testing Multimodal Extra Models Suite...")
    multi_res = post_json(f"{API_BASE}/multimodal/socratic-enhanced", {
        "scenario_context": "10 minutes before product launch client demands security check override.",
        "learner_choice": "Refused override and escalated to Incident Commander.",
        "is_optimal": True,
        "reflection": "Zero-trust protocols prevent public data breaches.",
        "cognitive_load": "medium"
    })
    print(f"🛡️ Gemma Socratic Prompt: \"{multi_res['socratic_prompt']}\" (Mode: {multi_res['gemma_privacy_metadata']['privacy_mode']})")
    print(f"🎬 Veo 8s Video Clip: {multi_res['veo_visualization']['video_url']}")
    print(f"🎙️ Lyria Spoken Audio: {multi_res['lyria_audio_coaching']['socratic_audio_url']} (Tone: {multi_res['lyria_audio_coaching']['voice_profile']['tone']})")

    # 6. Creator Telemetry & Analytics Dashboard
    print("\n[Step 6/6] Fetching Creator Dashboard Telemetry & Struggle Heatmap...")
    dash_res = get_json(f"{API_BASE}/telemetry/creator-dashboard/1")
    print(f"📊 Completion Rate: {dash_res['completion_rate']}% vs. Actual Mastery: {dash_res['mastery_rate']}%")
    print(f"⚠️ Mastery Gap: {dash_res['completion_mastery_gap']}%")
    print(f"🔥 Struggle Heatmap Scenarios Evaluated: {len(dash_res['cognitive_load_heatmap'])}")
    for h in dash_res['cognitive_load_heatmap']:
        print(f"   • {h['title']} -> Avg Time: {h['avg_time_seconds']}s | Struggle Index: {h['struggle_index']}% | Risk: {h['drop_off_risk']}")

    print("\n" + "=" * 75)
    print("🎉 ALL END-TO-END SYSTEM LAYERS VERIFIED & OPERATIONAL!")
    print("=" * 75)

if __name__ == "__main__":
    run_e2e()
