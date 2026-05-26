"use client";
import React, { useState } from "react";

type VarkScores = Record<string, number>;

type FinalResult = {
  scores: VarkScores;
  dominant: string;
  recommendations: {
    data?: {
      strategies?: string[];
      tools?: string[];
      personalized_tips?: string[];
    };
  };
  storage: unknown;
} | null;

const ChatPopup: React.FC = () => {
  
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<{ role: string; text: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [conversationContext, setConversationContext] = useState<string[]>([]);
  const [concluded, setConcluded] = useState(false);
  const [finalResult, setFinalResult] = useState<FinalResult>(null);

  return (
    <div className="chat-popup mx-auto mt-20 relative flex w-full justify-center">
      <div className="chat-scene relative flex items-end">
        
        {/* 15 individually positioned stars to avoid clumping */}
        {[
          { left: "calc(-20% - 20px)", top: "calc(-30% - 10px)", delay: "0s" },
          { left: "calc(0% - 10px)", top: "calc(-10% - 6px)", delay: "0.2s" },
          { left: "calc(12% - 6px)", top: "calc(-22% - 10px)", delay: "0.4s" },
          { left: "calc(28% - 8px)", top: "calc(-8% - 6px)", delay: "0.6s" },
          { left: "calc(46% - 4px)", top: "calc(-28% - 14px)", delay: "0.3s" },
          { left: "calc(68% - 10px)", top: "calc(-12% - 8px)", delay: "0.5s" },
          { left: "calc(96% + 6px)", top: "calc(-26% - 12px)", delay: "0.2s" },
          { left: "calc(-18% - 8px)", top: "calc(40% + 6px)", delay: "0.7s" },
          { left: "calc(6% - 6px)", top: "calc(82% + 10px)", delay: "0.4s" },
          { left: "calc(30% - 8px)", top: "calc(64% + 8px)", delay: "0.9s" },
          { left: "calc(52% - 6px)", top: "calc(78% + 12px)", delay: "0.2s" },
          { left: "calc(74% - 10px)", top: "calc(62% + 6px)", delay: "0.6s" },
          { left: "calc(110% + 12px)", top: "calc(74% + 8px)", delay: "0.8s" },
          { left: "calc(50% - 10px)", top: "calc(-40% - 18px)", delay: "0.15s" },
          { left: "calc(18% - 8px)", top: "calc(100% + 18px)", delay: "0.35s" },
        ].map((s, i) => (
          <span key={i} className={`chat-star star-${i + 1}`} />
        ))}

        {/* floating planets around the chat area */}
        {[
          { left: "calc(-12% - 24px)", top: "calc(-48% - 24px)", size: 44, bg: "radial-gradient(circle at 30% 30%, #ffd4f0, #9b59ff)", delay: "0s" },
          { left: "calc(50% - 26px)", top: "calc(-1% - 5px)", size: 48, bg: "radial-gradient(circle at 30% 30%, #9be6ff, #6b8cff)", delay: "0.25s" },
          { left: "calc(100% + 12px)", top: "calc(-40% - 10px)", size: 40, bg: "radial-gradient(circle at 30% 30%, #ffd7a8, #ff7ab6)", delay: "0.6s" },
          { left: "calc(102% + 120px)", top: "20%", size: 38, bg: "radial-gradient(circle at 30% 30%, #c7a7ff, #5ee7a3)", delay: "0.2s" },
          { left: "calc(90% - 18px)", top: "calc(120% + 18px)", size: 46, bg: "radial-gradient(circle at 30% 30%, #9bffea, #4b6bff)", delay: "0.45s" },
          { left: "calc(10% - 18px)", top: "calc(130% + 24px)", size: 36, bg: "radial-gradient(circle at 30% 30%, #ffd4f0, #ffb86b)", delay: "0.15s" },
          { left: "calc(-18% - 22px)", top: "36%", size: 40, bg: "radial-gradient(circle at 30% 30%, #b99bff, #ff9bdb)", delay: "0.5s" }
        ].map((p, i) => (
          <div key={`planet-${i}`} className={`floating-planet planet-${i + 1}`} />
        ))}

        <div className="chat-box w-[720px] md:w-[640px] rounded-xl border border-white/10 bg-gradient-to-br from-[#0b1226]/80 via-[#241033]/60 to-[#0b1426]/80 p-8 text-lg text-gray-100 shadow-2xl z-20">
          <div className="flex items-center justify-between">
            {/* <h3 className="text-sm font-semibold">AI Study Assistant</h3> */}
          </div>

          <div className="mt-4 max-h-96 overflow-y-auto rounded bg-white/5 p-6 text-base text-gray-200">
            {messages.length === 0 && (
              <div>
                <p className="text-lg">🎓 Welcome to Study Space!</p>
                <hr className="my-3 border-white/10" />
                <p className="text-base">I'll help you discover your learning style.</p>
                <p className="mt-3 text-base text-gray-300">Type 'quit' or 'exit' to stop.</p>
                <p className="mt-3 text-base text-gray-300">Tell me about yourself as a learner.</p>
                <p className="mt-2 text-sm text-gray-400">For example: Do you prefer videos, reading, hands-on practice, or listening?</p>
              </div>
            )}

            {messages.map((m, i) => (
              <div key={i} className={`mb-4 ${m.role === "user" ? "text-right" : "text-left"}`}>
                <div className={`inline-block rounded-xl px-4 py-3 ${m.role === "user" ? "bg-white/10" : "bg-white/6"}`}>
                  <pre className="whitespace-pre-wrap text-base text-gray-200">{m.text}</pre>
                </div>
              </div>
            ))}

            {finalResult && (
              <div className="mt-3 rounded-xl border border-white/10 bg-gradient-to-br from-[#071226]/60 to-[#1b0f1f]/60 p-4 text-sm text-gray-100">
                <h4 className="text-sm font-semibold mb-2">Your VARK Profile</h4>
                <div className="space-y-2">
                  {Object.entries(finalResult.scores).map(([k, v]) => (
                    <div key={k} className="flex items-center gap-3">
                      <div className="w-24 text-xs text-gray-300">{k.charAt(0).toUpperCase()+k.slice(1)}</div>
                      <div className="flex-1 h-3 bg-white/10 rounded overflow-hidden">
                        <div className="h-3 bg-gradient-to-r from-pink-400 to-violet-500" style={{ width: `${v}%` }} />
                      </div>
                      <div className="w-12 text-right text-xs">{v}%</div>
                    </div>
                  ))}
                </div>
                <div className="mt-3">
                  <h5 className="text-xs font-semibold">Recommended Strategies</h5>
                  <ul className="list-disc list-inside text-xs mt-1">
                    {(finalResult.recommendations?.data?.strategies || []).slice(0,5).map((s: string, i: number) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
                <div className="mt-2">
                  <h5 className="text-xs font-semibold">Tools</h5>
                  <div className="text-xs mt-1">{(finalResult.recommendations?.data?.tools || []).join(', ')}</div>
                </div>
                {(finalResult.recommendations?.data?.personalized_tips?.length ?? 0) > 0 && (
                  <div className="mt-2">
                    <h5 className="text-xs font-semibold">Personalized Tips</h5>
                    <ul className="list-disc list-inside text-xs mt-1">
                      {finalResult.recommendations.data?.personalized_tips?.slice(0,3).map((t: string, i: number) => (
                        <li key={i}>{t}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {/* Storage is persisted server-side; do not expose spreadsheet link to users */}
              </div>
            )}
            {loading && <p className="text-base text-gray-300">Thinking…</p>}
            {concluded && (
              <div className="mt-2 rounded bg-white/3 p-2 text-xs text-gray-200">
                Session concluded. Click "Start New Session" to try again.
              </div>
            )}
          </div>

            <div className="mt-5 flex gap-3">
            <input
              aria-label="Type a message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type a question..."
                className="flex-1 rounded border border-white/10 bg-transparent px-4 py-3 text-lg text-white placeholder:text-gray-400"
            />
            <button
              disabled={concluded || loading}
              onClick={async () => {
                if (!message.trim()) return;
                const userText = message.trim();
                setMessages((m) => [...m, { role: "user", text: userText }]);
                setMessage("");
                // Append to conversation context for combined scoring
                setConversationContext((c) => {
                  const next = [...c, userText];
                  return next;
                });
                setLoading(true);
                try {
                  // Send the combined conversation context so the backend can analyze cumulatively
                  const combined = [...conversationContext, userText].join(" ");
                  const res = await fetch("http://localhost:8001/v1/process_quiz", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ session_id: sessionId, input: combined }),
                  });
                  const data = await res.json();
                  if (data.session_id) setSessionId(data.session_id);
                  const result = data.result || {};

                  // Handle low confidence: ask user for more detail
                  if (result.status === "low_confidence") {
                    const text = `I couldn't score that confidently (confidence: ${result.confidence || 0}%). Could you share more detail about how you like to learn?`;
                    setMessages((m) => [...m, { role: "assistant", text }]);
                    setLoading(false);
                    return;
                  }

                  // Handle incomplete
                  if (result.status === "incomplete") {
                    const missing = result.missing ? result.missing.join(', ') : 'details';
                    setMessages((m) => [...m, { role: "assistant", text: `I need more information: missing ${missing}.` }]);
                    setConcluded(true);
                    setLoading(false);
                    return;
                  }

                  // Handle error
                  if (result.status === "error") {
                    setMessages((m) => [...m, { role: "assistant", text: `Error: ${result.message || 'Unknown error'}` }]);
                    setLoading(false);
                    return;
                  }

                  // success or exists -> show scores and fetch recommendations
                  if (result.status === "success" || result.status === "exists") {
                    const scores = result.scores || {};
                    const dominant = result.dominant || '';
                    // VARK bars and formatted details will display scores; skip duplicate plain-text summary

                    // Fetch recommendations (via Next.js proxy)
                    try {
                      const recRes = await fetch(`http://localhost:8001/v1/recommendations`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ vark_result: { ...scores, dominant } }),
                      });
                      const recData = await recRes.json();
                      const storage = result.storage || null;
                      // Build final structured result for a nicer card
                      setFinalResult({ scores, dominant, recommendations: recData, storage });
                      setConcluded(true);
                    } catch (_err) {
                      setMessages((m) => [...m, { role: "assistant", text: `Error fetching recommendations.` }]);
                      setConcluded(true);
                    }
                  }
                } catch (_err) {
                  setMessages((m) => [...m, { role: "assistant", text: "Error connecting to backend." }]);
                } finally {
                  setLoading(false);
                }
              }}
              className="rounded bg-gradient-to-r from-pink-400 to-violet-500 px-5 py-3 text-lg font-semibold text-black shadow-lg"
            >
              Send
            </button>
            <button
              onClick={() => {
                // Reset session to start a fresh one
                setSessionId(null);
                setConversationContext([]);
                setMessages([]);
                setConcluded(false);
                setMessage("");
                setFinalResult(null);
              }}
              className="ml-2 rounded-lg bg-gradient-to-r from-cyan-400 to-green-400 px-5 py-3 text-lg font-semibold text-black shadow-md"
            >
              Start New Session
            </button>
          </div>
        </div>
        
      </div>
      {/* Chat is always open in the UI */}
    </div>
  );
};

export default ChatPopup;