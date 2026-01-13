import { useEffect, useRef, useState } from "react";
import "./Home.css";
import logo from "../assets/img/logo.png";
import ReactMarkdown from "react-markdown";


export default function Home() {
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState("");
  const [messages, setMessages] = useState([]); 
  const [isListening, setIsListening] = useState(false);
  const [isSending, setIsSending] = useState(false);

  const recognitionRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    setConversationId(crypto.randomUUID());
  }, []);

  // useEffect(() => {
  //   chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  // }, [messages]);

  const startVoice = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Désolé, la reconnaissance vocale n'est pas supportée sur ce navigateur.");
      return;
    }

    
    if (!recognitionRef.current) {
      const rec = new SpeechRecognition();
      rec.lang = "fr-FR";
      rec.interimResults = true;
      rec.continuous = false;

      rec.onresult = (e) => {
        const transcript = Array.from(e.results)
          .map((r) => r[0]?.transcript || "")
          .join("");
        setInput(transcript);
      };

      rec.onend = () => {
        setIsListening(false);
      };

      rec.onerror = () => {
        setIsListening(false);
      };

      recognitionRef.current = rec;
    }

    setIsListening(true);
    recognitionRef.current.start();
  };

  const stopVoice = () => {
    if (recognitionRef.current) recognitionRef.current.stop();
    setIsListening(false);
  };

  const send = async () => {
    const text = input.trim();
    if (!text || !conversationId || isSending) return;

    setMessages((prev) => [...prev, { role: "user", text }]);
    setInput("");
    setIsSending(true);

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
      setConversationId(data.conversation_id);
      setMessages((prev) => [...prev, { role: "bot", text: data.reply }]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Erreur: impossible de joindre le backend." },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const newChat = () => {
    setConversationId(crypto.randomUUID());
    setMessages([]);
    setInput("");
  };

  return (
    <div className="page">
      <div className="shootingStars">
        <div className="star"></div>
        <div className="star"></div>
        <div className="star"></div>
        <div className="star"></div>
        <div className="star"></div>
        <div className="star"></div>
        <div className="star"></div>
      </div>
      <main className="main">
        <header className="topbar">
          <div className="headerBrand">
            <img src={logo} alt="AstroBot" className="logoHeader" />
            <span className="brandName">AstroBot</span>
          </div>
          <div className="status">
            {isSending ? "Réponse en cours…" : isListening ? "Écoute…" : ""}
          </div>
        </header>

        <section className="chat">
          {messages.length === 0 && (
            <div className="welcomeMessage">
              <div className="welcomeIcon"></div>
              <h3>Explorez l'univers avec AstroBot</h3>
              <p>Posez vos questions sur l'astronomie, demandez l'APOD du jour ou les dernières actualités spatiales</p>
            </div>
          )}

          {messages.map((m, idx) => (
            <div key={idx} className={`msgRow ${m.role === "user" ? "right" : "left"}`}>
              <div className={`bubble ${m.role === "user" ? "user" : "bot"}`}>
                <div className="bubbleRole">{m.role === "user" ? "Moi" : "AstroBot"}</div>
                <div className="bubbleText">
                    {m.role === "bot" ? (
                      <ReactMarkdown
                        components={{
                          h3: ({ children }) => (
                            <div className="md-title">{children}</div>
                          ),
                          ul: ({ children }) => (
                            <ul className="md-list">{children}</ul>
                          ),
                          li: ({ children }) => (
                           <li className="md-list-item">
                             <span className="bullet">•</span>
                             <span className="content">{children}</span>
                            </li>
                         ),
                       }}
                      >
                        {m.text}
                     </ReactMarkdown>
                    ) : (
                      m.text
                    )}
                  </div>

              </div>
            </div>
          ))}

          <div ref={chatEndRef} />
        </section>

        <footer className="composer">
          <div className="inputWrap">
            <input
              className="input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="Tapez votre message ici…"
            />

            <button
              className={`iconBtn ${isListening ? "active" : ""}`}
              onClick={isListening ? stopVoice : startVoice}
              title={isListening ? "Arrêter la dictée" : "Dicter (micro)"}
              type="button"
            >
              {isListening ? "⏹️" : "🎙️"}
            </button>

            <button className="sendBtn" onClick={send} disabled={isSending} type="button">
              {isSending ? "…" : "➤"}
            </button>
          </div>

          <div className="footerNote">
            IA locale via Ollama • Données live via MCP tools • React UI
          </div>
        </footer>
      </main>
    </div>
  );
}



