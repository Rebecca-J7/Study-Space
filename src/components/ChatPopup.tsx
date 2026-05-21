"use client";
import React, { useState } from "react";

const ChatPopup: React.FC = () => {
  const [open, setOpen] = useState(true);
  const [message, setMessage] = useState("");

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

        <div className="chat-box w-[560px] md:w-[480px] rounded-xl border border-white/10 bg-gradient-to-br from-[#0b1226]/80 via-[#241033]/60 to-[#0b1426]/80 p-6 text-base text-gray-100 shadow-2xl z-20">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold">AI Study Assistant</h3>
            <button
              aria-label="Close chat"
              className="text-sm text-gray-300"
              onClick={() => setOpen(false)}
            >
              ✕
            </button>
          </div>

          <div className="mt-3 max-h-80 overflow-y-auto rounded bg-white/5 p-4 text-sm text-gray-200">
            <p className="text-sm text-gray-400">This is a placeholder chat area.</p>
            <p className="mt-2 text-sm text-gray-300">The AI chat will appear here in a future update.</p>
          </div>

          <div className="mt-4 flex gap-3">
            <input
              aria-label="Type a message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type a question..."
              className="flex-1 rounded border border-white/10 bg-transparent px-3 py-2 text-base text-white placeholder:text-gray-400"
            />
            <button
              onClick={() => {
                setMessage("");
              }}
              className="rounded bg-gradient-to-r from-pink-400 to-violet-500 px-4 py-2 text-base font-semibold text-black"
            >
              Send
            </button>
          </div>
        </div>
        
      </div>
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="mt-2 rounded-full bg-web-purple-2 px-4 py-2 font-semibold text-white shadow-lg"
        >
          Open Chat
        </button>
      )}
    </div>
  );
};

export default ChatPopup;
