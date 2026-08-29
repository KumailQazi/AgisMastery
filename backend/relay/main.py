import os
import json
import time
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

try:
    import redis.asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api")
SESSION_TTL_ACTIVE = int(os.environ.get("SESSION_TTL_ACTIVE_SECONDS", "3600"))
SESSION_TTL_DISCONNECTED = int(os.environ.get("SESSION_TTL_DISCONNECTED_SECONDS", "86400"))

app = FastAPI(
    title="Mastery Session Relay Service",
    description="Real-time WebSocket session relay and state synchronization with Redis and Firestore.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session fallback if Redis is offline
memory_session_store: Dict[str, Dict[str, Any]] = {}
redis_client = None

@app.on_event("startup")
async def startup_event():
    global redis_client
    if REDIS_AVAILABLE:
        try:
            redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
            await redis_client.ping()
        except Exception:
            redis_client = None

async def save_session_state(session_id: str, state: Dict[str, Any], ttl: int = SESSION_TTL_ACTIVE):
    state["updated_at"] = time.time()
    if redis_client:
        try:
            await redis_client.setex(f"session:{session_id}", ttl, json.dumps(state))
            return
        except Exception:
            pass
    memory_session_store[session_id] = state

async def get_session_state(session_id: str) -> Optional[Dict[str, Any]]:
    if redis_client:
        try:
            raw = await redis_client.get(f"session:{session_id}")
            if raw:
                return json.loads(raw)
        except Exception:
            pass
    return memory_session_store.get(session_id)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "mastery-relay",
        "redis_connected": redis_client is not None,
        "active_memory_sessions": len(memory_session_store)
    }

@app.get("/session/{session_id}")
async def resume_session(session_id: str):
    state = await get_session_state(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    return {"session_id": session_id, "state": state, "resumable": True}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    # Load or initialize session state
    session_state = await get_session_state(session_id) or {
        "session_id": session_id,
        "connected_at": time.time(),
        "interactions": [],
        "current_scaffolding_level": 2,
        "mastery_count": 0
    }
    await save_session_state(session_id, session_state, ttl=SESSION_TTL_ACTIVE)

    # Send initial session handshake
    await websocket.send_json({
        "type": "session_ready",
        "session_id": session_id,
        "state": session_state
    })

    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")
            payload = data.get("payload", {})

            # 1. Event: Decision Submitted
            if event_type == "decision_submitted":
                branch_id = payload.get("branch_id")
                scenario_id = payload.get("scenario_id", 1)
                is_optimal = payload.get("is_optimal", False)

                # Call core mastery-api to execute ADK Socratic loop
                socratic_prompt = ""
                consequence = ""
                try:
                    async with httpx.AsyncClient() as client:
                        resp = await client.post(
                            f"{API_BASE_URL}/scenarios/{scenario_id}/decide",
                            json={
                                "learner_id": payload.get("learner_id", 1),
                                "branch_id": branch_id,
                                "time_spent_seconds": payload.get("time_spent_seconds", 10.0),
                                "hints_used": payload.get("hints_used", ""),
                                "cognitive_load_signal": payload.get("cognitive_load_signal", "normal")
                            },
                            timeout=5.0
                        )
                        if resp.status_code == 200:
                            api_res = resp.json()
                            socratic_prompt = api_res.get("socratic_prompt")
                            consequence = api_res.get("consequence")
                except Exception:
                    pass

                if not socratic_prompt:
                    if is_optimal:
                        socratic_prompt = "Strong choice under pressure. What principle guided your decision over the alternative?"
                        consequence = "Protocol was preserved cleanly with zero leakage."
                    else:
                        socratic_prompt = "You chose speed over verification. What consequence followed, and how would you handle the tradeoff next time?"
                        consequence = "An unexpected vulnerability was introduced."

                session_state["interactions"].append({
                    "event": "decision",
                    "branch_id": branch_id,
                    "is_optimal": is_optimal,
                    "timestamp": time.time()
                })
                await save_session_state(session_id, session_state)

                await websocket.send_json({
                    "type": "socratic_prompt",
                    "consequence": consequence,
                    "socratic_prompt": socratic_prompt,
                    "is_optimal": is_optimal
                })

            # 2. Event: Cognitive Load Update (Silent Telemetry)
            elif event_type == "cognitive_load_update":
                hesitation_seconds = payload.get("hesitation_seconds", 0)
                signal = "high_hesitation" if hesitation_seconds > 10 else "normal"
                
                adjustment = {
                    "signal": signal,
                    "suggest_scaffolding": hesitation_seconds > 12,
                    "action": "offer_hint" if hesitation_seconds > 12 else "maintain"
                }

                await websocket.send_json({
                    "type": "flow_state_adjustment",
                    "adjustment": adjustment
                })

            # 3. Event: Reflection Submitted
            elif event_type == "reflection_submitted":
                reflection_text = payload.get("reflection_text", "")
                
                feedback = (
                    f"Insightful reflection. You articulated the balance between speed and reliability. "
                    f"Ready to advance to the next scenario variation."
                )

                session_state["interactions"].append({
                    "event": "reflection",
                    "reflection_text": reflection_text,
                    "timestamp": time.time()
                })
                await save_session_state(session_id, session_state)

                await websocket.send_json({
                    "type": "reflection_feedback",
                    "feedback": feedback,
                    "advance_ready": True
                })

    except WebSocketDisconnect:
        # On disconnect, extend TTL to 24 hours so session can be resumed later
        await save_session_state(session_id, session_state, ttl=SESSION_TTL_DISCONNECTED)
    except Exception as e:
        await websocket.close()
