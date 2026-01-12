import { useEffect, useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState("");
  const [messages, setMessages] = useState([]); // {role, text}

  // Génère un conversation_id une fois (simple)
  useEffect(() => {
    setConversationId(crypto.randomUUID());
  }, []);

  const send = async () => {
    const text = input.trim();
    if (!text || !conversationId) return;

    setMessages((prev) => [...prev, { role: "user", text }]);
    setInput("");

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          conversation_id: conversationId,
        }),
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(errText);
      }

      const data = await res.json();

      // Backend renvoie reply + conversation_id
      setConversationId(data.conversation_id);
      setMessages((prev) => [...prev, { role: "bot", text: data.reply }]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Erreur: impossible de joindre le backend." },
      ]);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", fontFamily: "Arial" }}>
      <h2>Astro Bot</h2>

      <div style={{ border: "1px solid #ddd", borderRadius: 10, padding: 12, minHeight: 320 }}>
        {messages.map((m, idx) => (
          <div key={idx} style={{ margin: "10px 0" }}>
            <b>{m.role === "user" ? "Moi" : "Bot"}:</b> {m.text}
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Écris un message..."
          style={{ flex: 1, padding: 10, borderRadius: 10, border: "1px solid #ddd" }}
        />
        <button onClick={send} style={{ padding: "10px 16px", borderRadius: 10 }}>
          Envoyer
        </button>
      </div>

      <p style={{ fontSize: 12, opacity: 0.6 }}>conversation_id: {conversationId}</p>
    </div>
  );
}

export default App;
