import { useState } from "react";
import { generateEmail } from "./api";
import type { EmailResponse } from "./api";
import { MessageInput } from "./components/MessageInput";
import { EmailResult } from "./components/EmailResult";
import { LoadingDots } from "./components/LoadingDots";
import "./App.css";

export default function App() {
  const [message, setMessage] = useState("");
  const [recipient, setRecipient] = useState("colleague");
  const [result, setResult] = useState<EmailResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit() {
    if (!message.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await generateEmail(message, recipient);
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <p className="eyebrow">日本語ビジネスメール</p>
        <h1>Japanese Business <em>Email Agent</em></h1>
        <p className="subtitle">Write casually → get 3 levels of keigo-perfect Japanese email</p>
      </header>

      <main className="main">
        <MessageInput
          message={message}
          recipient={recipient}
          loading={loading}
          onChange={setMessage}
          onRecipientChange={setRecipient}
          onSubmit={handleSubmit}
        />

        {error && <p className="error">{error}</p>}
        {loading && <LoadingDots />}
        {result && <EmailResult result={result} />}
      </main>
    </div>
  );
}
