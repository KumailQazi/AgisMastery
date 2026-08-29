import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Custom hook for managing real-time WebSocket connection to the Mastery Session Relay.
 * Handles auto-reconnect, typed message parsing, and telemetry signal streaming.
 */
export function useWebSocket(sessionId, relayUrl = 'ws://localhost:8080') {
  const [isConnected, setIsConnected] = useState(false);
  const [sessionState, setSessionState] = useState(null);
  const [socraticPrompt, setSocraticPrompt] = useState(null);
  const [flowState, setFlowState] = useState(null);
  const [reflectionFeedback, setReflectionFeedback] = useState(null);

  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const connect = useCallback(() => {
    if (!sessionId) return;

    const wsUrl = `${relayUrl}/ws/${sessionId}`;
    const ws = new WebSocket(wsUrl);
    socketRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      console.log(`[Mastery Relay] Connected to session ${sessionId}`);
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        const { type } = message;

        switch (type) {
          case 'session_ready':
            setSessionState(message.state);
            break;
          case 'socratic_prompt':
            setSocraticPrompt({
              consequence: message.consequence,
              prompt: message.socratic_prompt,
              isOptimal: message.is_optimal,
            });
            break;
          case 'flow_state_adjustment':
            setFlowState(message.adjustment);
            break;
          case 'reflection_feedback':
            setReflectionFeedback(message.feedback);
            break;
          default:
            console.log('[Mastery Relay] Unhandled message type:', type);
        }
      } catch (err) {
        console.error('[Mastery Relay] Error parsing message:', err);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log('[Mastery Relay] Disconnected. Attempting reconnect in 3s...');
      reconnectTimeoutRef.current = setTimeout(connect, 3000);
    };

    ws.onerror = (err) => {
      console.error('[Mastery Relay] WebSocket error:', err);
      ws.close();
    };
  }, [sessionId, relayUrl]);

  useEffect(() => {
    connect();
    return () => {
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      if (socketRef.current) socketRef.current.close();
    };
  }, [connect]);

  const sendEvent = useCallback((type, payload) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type, payload }));
    } else {
      console.warn('[Mastery Relay] Socket not open, message queued or dropped');
    }
  }, []);

  const sendDecision = useCallback((decisionData) => {
    sendEvent('decision_submitted', decisionData);
  }, [sendEvent]);

  const sendCognitiveLoad = useCallback((loadData) => {
    sendEvent('cognitive_load_update', loadData);
  }, [sendEvent]);

  const sendReflection = useCallback((reflectionData) => {
    sendEvent('reflection_submitted', reflectionData);
  }, [sendEvent]);

  return {
    isConnected,
    sessionState,
    socraticPrompt,
    flowState,
    reflectionFeedback,
    sendDecision,
    sendCognitiveLoad,
    sendReflection,
  };
}
