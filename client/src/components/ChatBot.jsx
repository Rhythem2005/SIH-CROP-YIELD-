// src/components/ChatBot.jsx

import React, { useState, useRef, useEffect } from "react";
import { API_ENDPOINTS } from "../utils/apiConfig";

export default function ChatBot() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "🌾 Namaste! I am Kisan Mitra. I am here to answer your farming-related questions. 😊"
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);
    setInput("");
    setLoading(true);

    try {
      // ✅ Call backend API instead of Gemini directly
      const response = await fetch(API_ENDPOINTS.CHAT, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      const responseText = data.response || "Maaf kijiye, iska jawab mujhe abhi nahi pata. 😅";

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: responseText }
      ]);
    } catch (err) {
      console.error("Error in chatbot response:", err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Oops! Koi error ho gaya. Kripya dobara try karein." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating Button */}
      <div className="fixed bottom-5 right-5 z-50">
        <button
          onClick={() => setOpen(!open)}
          className="bg-green-600 hover:bg-green-700 text-white p-4 rounded-full shadow-lg text-xl"
        >
          🌾
        </button>
      </div>

      {/* Chat Window */}
      {open && (
        <div className="fixed bottom-20 right-5 z-50 w-80 max-h-[500px] flex flex-col bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Header */}
          <div className="bg-green-600 text-white p-3 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Kisan Mitra 🌾</h2>
            <button onClick={() => setOpen(false)} className="text-xl hover:text-gray-200">✖</button>
          </div>

          {/* Chat Area */}
          <div className="flex-1 p-3 overflow-y-auto space-y-2 bg-green-50">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[70%] p-2 rounded-xl whitespace-pre-line ${
                    msg.sender === "user"
                      ? "bg-green-600 text-white rounded-br-none"
                      : "bg-white text-gray-800 rounded-bl-none shadow"
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="max-w-[70%] p-2 rounded-xl bg-gray-200 text-gray-700 animate-pulse">
                  Typing...
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-2 bg-green-100 flex gap-2">
            <input
              type="text"
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              className="flex-1 border rounded-full px-3 py-1 focus:outline-none focus:ring-2 focus:ring-green-400"
            />
            <button
              onClick={sendMessage}
              className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded-full font-medium transition"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
}
