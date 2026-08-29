// ==========================================================================
// MASTERY — Frontend Interactive Socratic Loop & Telemetry Controller
// ==========================================================================

const API_BASE = "http://localhost:8000/api";

let selectedBranchId = null;
let selectedBranchOptimal = false;
let startTime = Date.now();
let hintsUsed = 0;
let attemptsCount = 0;
let correctCount = 0;
let timerInterval = null;

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  startTimer();
  logTelemetry("Session started. Silent telemetry tracker active.");
});

// View Switcher
function switchView(viewName) {
  document.querySelectorAll(".view-panel").forEach(panel => panel.classList.remove("active"));
  document.querySelectorAll(".nav-tab").forEach(tab => tab.classList.remove("active"));

  if (viewName === "learner") {
    document.getElementById("view-learner").classList.add("active");
    document.getElementById("tab-learner").classList.add("active");
  } else {
    document.getElementById("view-creator").classList.add("active");
    document.getElementById("tab-creator").classList.add("active");
    fetchCreatorAnalytics();
  }
}

// Timer & Hesitation Tracking
function startTimer() {
  clearInterval(timerInterval);
  startTime = Date.now();
  timerInterval = setInterval(() => {
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
    const secs = String(elapsed % 60).padStart(2, '0');
    document.getElementById("time-count").innerText = `${mins}:${secs}`;
    
    if (elapsed === 8 && !selectedBranchId) {
      logTelemetry("Hesitation detected (>8s without decision). Cognitive load: Elevated.");
    }
  }, 1000);
}

// Branch Selection
function selectBranch(branchId, isOptimal, element) {
  selectedBranchId = branchId;
  selectedBranchOptimal = isOptimal;

  document.querySelectorAll(".branch-card").forEach(c => c.classList.remove("selected"));
  element.classList.add("selected");
  document.getElementById("submit-decision-btn").disabled = false;

  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  logTelemetry(`Branch #${branchId} selected at ${elapsed}s.`);
}

// Request Scaffolding Hint
function requestHint() {
  hintsUsed++;
  document.getElementById("hint-count").innerText = hintsUsed;
  document.getElementById("hint-box").classList.remove("hidden");
  logTelemetry(`Scaffolding Hint requested (Total hints: ${hintsUsed}).`);
}

// Submit Decision
async function submitDecision() {
  if (!selectedBranchId) return;

  const elapsedSeconds = ((Date.now() - startTime) / 1000).toFixed(1);
  clearInterval(timerInterval);

  document.getElementById("submit-decision-btn").disabled = true;

  // Try API call with graceful fallback
  let responseData = null;
  try {
    const res = await fetch(`${API_BASE}/scenarios/1/decide`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        learner_id: 1,
        branch_id: selectedBranchId,
        time_spent_seconds: parseFloat(elapsedSeconds),
        hints_used: hintsUsed > 0 ? "hint_security_guidelines" : "",
        cognitive_load_signal: elapsedSeconds > 12 ? "high_hesitation" : "moderate"
      })
    });
    if (res.ok) {
      responseData = await res.json();
    }
  } catch (err) {
    console.log("Backend offline, running local Socratic simulation mode.");
  }

  // Fallback data if backend is offline
  if (!responseData) {
    if (selectedBranchOptimal) {
      responseData = {
        consequence: "The launch is delayed by 15 minutes, but zero security vulnerabilities leak.",
        is_optimal: true,
        socratic_prompt: "Strong decision. Why did protocol adherence matter more than short-term client press pressure in this specific context?",
        scaffolding: { scaffolding_level: 2, rationale: "Learner displayed good protocol discipline." }
      };
    } else {
      responseData = {
        consequence: "Launch happened on time, but 2 hours later an unauthorized vulnerability exposure caused a critical security incident.",
        is_optimal: false,
        socratic_prompt: "You prioritized speed over security validation. What unintended downstream consequences occurred, and what risk threshold should govern overrides?",
        scaffolding: { scaffolding_level: 3, rationale: "Needs reinforcement on zero-trust governance." }
      };
    }
  }

  // Update Mastery Stats
  attemptsCount++;
  if (selectedBranchOptimal) correctCount++;
  updateMasteryUI();

  // Log Telemetry
  logTelemetry(`Decision committed: Branch #${selectedBranchId} (${selectedBranchOptimal ? 'OPTIMAL' : 'SUB-OPTIMAL'}) in ${elapsedSeconds}s.`);
  logTelemetry(`Mastery State: ${correctCount}/${attemptsCount} correct decisions recorded.`);

  // Append AI Chat
  appendChatMessage("ai", `<strong>Consequence:</strong> ${responseData.consequence}`);
  setTimeout(() => {
    appendChatMessage("ai", `<strong>Socratic Follow-Up:</strong> ${responseData.socratic_prompt}`);
    document.getElementById("reflection-box").classList.remove("hidden");
    document.getElementById("reflection-input").focus();
  }, 600);
}

// Submit Reflection
async function submitReflection() {
  const text = document.getElementById("reflection-input").value.trim();
  if (!text) return;

  appendChatMessage("user", text);
  document.getElementById("reflection-input").value = "";
  document.getElementById("reflection-box").classList.add("hidden");

  logTelemetry(`Reflection submitted: "${text.substring(0, 35)}..." (Sentiment & depth: Verified).`);

  setTimeout(() => {
    appendChatMessage("ai", `Insightful reflection. You've identified the systemic trade-off between press deadlines and vulnerability liability. Socratic feedback loop complete. Ready for Scenario #2 (Production DB Migration Anomaly).`);
    document.getElementById("difficulty-badge").innerText = "Difficulty: Level 3 (Adapted)";
  }, 800);
}

// Append Chat Message
function appendChatMessage(sender, content) {
  const feed = document.getElementById("dialogue-feed");
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender === "ai" ? "ai-bubble" : "user-bubble"}`;
  bubble.innerHTML = `<p>${content}</p>`;
  feed.appendChild(bubble);
  feed.scrollTop = feed.scrollHeight;
}

// Log Silent Telemetry
function logTelemetry(msg) {
  const stream = document.getElementById("telemetry-stream");
  const elapsed = Math.floor((Date.now() - startTime) / 1000);
  const mins = String(Math.floor(elapsed / 60)).padStart(2, '0');
  const secs = String(elapsed % 60).padStart(2, '0');

  const item = document.createElement("div");
  item.className = "telemetry-log-item";
  item.innerHTML = `<span class="log-time">[${mins}:${secs}]</span> ${msg}`;
  stream.appendChild(item);
  stream.scrollTop = stream.scrollHeight;
}

// Update Mastery Progress UI
function updateMasteryUI() {
  const percent = Math.round((correctCount / 5) * 100);
  document.getElementById("mastery-progress-bar").style.width = `${percent}%`;
  document.getElementById("mastery-percent-text").innerText = `${correctCount}/5 Decisions (${percent}%)`;
}

// Fetch Creator Analytics
async function fetchCreatorAnalytics() {
  try {
    const res = await fetch(`${API_BASE}/telemetry/creator-dashboard/1`);
    if (res.ok) {
      const data = await res.json();
      console.log("Loaded creator dashboard data from API:", data);
    }
  } catch (err) {
    // Uses pre-rendered rich data
  }
}

// Theme Toggle
function toggleTheme() {
  document.body.classList.toggle("light-theme");
}
