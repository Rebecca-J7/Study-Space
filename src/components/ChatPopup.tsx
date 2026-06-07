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
} | null;

type Phase = "quiz" | "elaborate" | "followup" | "concluded";

const ChatPopup: React.FC = () => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<{ role: string; text: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [phase, setPhase] = useState<Phase>("quiz");
  const [questionNumber, setQuestionNumber] = useState(0);
  const [finalResult, setFinalResult] = useState<FinalResult>(null);

  const addMessage = (role: string, text: string) => {
    setMessages((m) => [...m, { role, text }]);
  };

  const fetchRecommendations = async (scores: VarkScores, dominant: string) => {
    try {
      const recRes = await fetch("/api/study-space/v1/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ vark_result: { ...scores, dominant } }),
      });
      const recData = await recRes.json();
      setFinalResult({ scores, dominant, recommendations: recData });
    } catch {
      addMessage("assistant", "Error fetching recommendations.");
    }
  };

  const handleResult = async (result: Record<string, unknown>, _sid: string) => {
    if (result.status === "low_confidence") {
      const confidence = result.confidence as number || 0;
      addMessage("assistant",
        `🤔 Your responses were a bit vague (confidence: ${confidence}%).\n` +
        `Could you share more detail about how you like to learn?\n` +
        `For example: Do you prefer videos, diagrams, reading, or hands-on practice?\n` +
        `Type 'done' to score anyway.`
      );
      setPhase("elaborate");
      return;
    }

    if (result.status === "incomplete") {
      const missing = (result.missing as string[] || []).join(", ");
      addMessage("assistant", `❌ Missing information: ${missing}. Please try again.`);
      setPhase("concluded");
      return;
    }

    if (result.status === "error") {
      addMessage("assistant", `❌ Error: ${result.message || "Unknown error"}`);
      return;
    }

    if (result.status === "success" || result.status === "exists") {
      const scores = result.scores as VarkScores || {};
      const dominant = result.dominant as string || "";
      addMessage("assistant",
        `✅ Your VARK profile has been saved!\n🏆 Dominant Style: ${dominant} Learner\n\n` +
        `💬 Want to ask anything about your learning style?\nType your question or 'done' to finish.`
      );
      await fetchRecommendations(scores, dominant);
      setPhase("followup");
    }
  };

  // Start quiz on first load
  const startQuiz = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/study-space/v1/quiz/start", { method: "POST" });
      const data = await res.json();
      setSessionId(data.session_id);
      setQuestionNumber(1);
      addMessage("assistant", `${data.question}`);
    } catch {
      addMessage("assistant", "Error starting quiz. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!message.trim()) return;
    const userText = message.trim();
    addMessage("user", userText);
    setMessage("");
    setLoading(true);

    try {
      // Handle quit
      if (["quit", "exit"].includes(userText.toLowerCase())) {
        addMessage("assistant", "👋 Thanks for using Study Space! Good luck studying!");
        setPhase("concluded");
        setLoading(false);
        return;
      }

      // Phase: quiz — answering structured questions
      if (phase === "quiz") {
        const res = await fetch("/api/study-space/v1/quiz/answer", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, answer: userText }),
        });
        const data = await res.json();

        if (data.status === "in_progress") {
          setQuestionNumber(data.question_number);
          addMessage("assistant", data.question);
        } else {
          await handleResult(data.result, data.session_id);
        }
        return;
      }

      // Phase: elaborate — low confidence, asking for more detail
      if (phase === "elaborate") {
        if (["done", "finished"].includes(userText.toLowerCase())) {
          // Force score with existing answers
          const res = await fetch("/api/study-space/v1/quiz/elaborate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, answer: userText }),
          });
          const data = await res.json();
          await handleResult(data.result, data.session_id);
          return;
        }

        const res = await fetch("/api/study-space/v1/quiz/elaborate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, answer: userText }),
        });
        const data = await res.json();
        await handleResult(data.result, data.session_id);
        return;
      }

      // Phase: followup — post-results Q&A
      if (phase === "followup") {
        if (["done", "finished"].includes(userText.toLowerCase())) {
          addMessage("assistant", "👋 Thanks for using Study Space! Good luck studying!");
          setPhase("concluded");
          return;
        }

        const res = await fetch("/api/study-space/v1/quiz/followup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: sessionId, question: userText }),
        });
        const data = await res.json();
        addMessage("assistant", `💡 ${data.answer}`);
        return;
      }

    } catch {
      addMessage("assistant", "Error connecting to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-popup mx-auto mt-20 relative flex w-full justify-center">
      <div className="chat-scene relative flex items-end">

        {/* Stars */}
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

        {/* Planets */}
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

          <div className="mt-4 max-h-96 overflow-y-auto rounded bg-white/5 p-6 text-base text-gray-200">

            {/* Welcome screen before quiz starts */}
            {messages.length === 0 && (
              <div>
                <p className="text-lg">🎓 Welcome to Study Space!</p>
                <hr className="my-3 border-white/10" />
                <p className="text-base">I'll ask you 5 questions to discover your VARK learning style.</p>
                <p className="mt-3 text-sm text-gray-400">Click "Start Quiz" to begin!</p>
              </div>
            )}

            {/* Chat messages */}
            {messages.map((m, i) => (
              <div key={i} className={`mb-4 ${m.role === "user" ? "text-right" : "text-left"}`}>
                <div className={`inline-block rounded-xl px-4 py-3 ${m.role === "user" ? "bg-white/10" : "bg-white/6"}`}>
                  <pre className="whitespace-pre-wrap text-base text-gray-200">{m.text}</pre>
                </div>
              </div>
            ))}

            {/* VARK Results Card */}
            {finalResult && (
              <div className="mt-3 rounded-xl border border-white/10 bg-gradient-to-br from-[#071226]/60 to-[#1b0f1f]/60 p-4 text-sm text-gray-100">
                <h4 className="text-sm font-semibold mb-2">📊 Your VARK Profile</h4>
                <div className="space-y-2">
                  {Object.entries(finalResult.scores).map(([k, v]) => (
                    <div key={k} className="flex items-center gap-3">
                      <div className="w-24 text-xs text-gray-300">{k.charAt(0).toUpperCase() + k.slice(1)}</div>
                      <div className="flex-1 h-3 bg-white/10 rounded overflow-hidden">
                        <div className="h-3 bg-gradient-to-r from-pink-400 to-violet-500" style={{ width: `${v}%` }} />
                      </div>
                      <div className="w-12 text-right text-xs">{v}%</div>
                    </div>
                  ))}
                </div>
                <div className="mt-3">
                  <h5 className="text-xs font-semibold">📚 Recommended Strategies</h5>
                  <ul className="list-disc list-inside text-xs mt-1">
                    {(finalResult.recommendations?.data?.strategies || []).slice(0, 5).map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
                <div className="mt-2">
                  <h5 className="text-xs font-semibold">🛠 Tools</h5>
                  <div className="text-xs mt-1">{(finalResult.recommendations?.data?.tools || []).join(", ")}</div>
                </div>
                {(finalResult.recommendations?.data?.personalized_tips?.length ?? 0) > 0 && (
                  <div className="mt-2">
                    <h5 className="text-xs font-semibold">✨ Personalized Tips</h5>
                    <ul className="list-disc list-inside text-xs mt-1">
                      {finalResult.recommendations.data?.personalized_tips?.slice(0, 3).map((t, i) => (
                        <li key={i}>{t}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {loading && <p className="text-base text-gray-300">Thinking…</p>}

            {phase === "concluded" && (
              <div className="mt-2 rounded bg-white/5 p-2 text-xs text-gray-300">
                Session concluded. Click "Start New Session" to try again.
              </div>
            )}
          </div>

          {/* Input area */}
          <div className="mt-5 flex gap-3">
            {/* Show Start Quiz button before quiz begins */}
            {messages.length === 0 ? (
              <button
                onClick={startQuiz}
                disabled={loading}
                className="w-full rounded bg-gradient-to-r from-pink-400 to-violet-500 px-5 py-3 text-lg font-semibold text-black shadow-lg"
              >
                🚀 Start Quiz
              </button>
            ) : (
              <>
                <input
                  aria-label="Type a message"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && !loading && handleSend()}
                  placeholder={
                    phase === "followup" ? "Ask a question about your results..." :
                    phase === "elaborate" ? "Share more detail, or type 'done'..." :
                    phase === "concluded" ? "Session ended." :
                    "Type your answer..."
                  }
                  disabled={phase === "concluded" || loading}
                  className="flex-1 rounded border border-white/10 bg-transparent px-4 py-3 text-lg text-white placeholder:text-gray-400"
                />
                <button
                  disabled={phase === "concluded" || loading}
                  onClick={handleSend}
                  className="rounded bg-gradient-to-r from-pink-400 to-violet-500 px-5 py-3 text-lg font-semibold text-black shadow-lg"
                >
                  Send
                </button>
              </>
            )}
            <button
              onClick={() => {
                setSessionId(null);
                setMessages([]);
                setPhase("quiz");
                setQuestionNumber(0);
                setMessage("");
                setFinalResult(null);
              }}
              className="ml-2 rounded-lg bg-gradient-to-r from-cyan-400 to-green-400 px-5 py-3 text-lg font-semibold text-black shadow-md"
            >
              Start New Session
            </button>
          </div>

          {/* Progress indicator during quiz */}
          {phase === "quiz" && questionNumber > 0 && (
            <div className="mt-3 text-xs text-gray-400 text-center">
              Question {questionNumber} of 5
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatPopup;