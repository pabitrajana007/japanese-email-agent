const SCENARIOS = [
  "Can we move tomorrow's meeting to 3pm?",
  "I need 2 more days to finish the report.",
  "Thanks for your help with the project.",
  "Sorry for the delay in my response.",
  "Just following up on my previous email.",
];

const RECIPIENTS = [
  { value: "colleague", label: "Colleague (同僚)" },
  { value: "direct manager", label: "Manager (上司)" },
  { value: "senior executive", label: "Executive (役員)" },
  { value: "external client", label: "Client (取引先)" },
  { value: "new business contact", label: "New contact (初めての方)" },
];

interface Props {
  message: string;
  recipient: string;
  loading: boolean;
  onChange: (message: string) => void;
  onRecipientChange: (recipient: string) => void;
  onSubmit: () => void;
}

export function MessageInput({ message, recipient, loading, onChange, onRecipientChange, onSubmit }: Props) {
  return (
    <div className="input-section">
      {/* Quick scenario chips */}
      <div className="chips">
        {SCENARIOS.map((s) => (
          <button key={s} className="chip" onClick={() => onChange(s)}>
            {s.slice(0, 30)}…
          </button>
        ))}
      </div>

      {/* Message textarea */}
      <textarea
        className="textarea"
        rows={4}
        placeholder="Write your message in English or casual Japanese..."
        value={message}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => { if ((e.metaKey || e.ctrlKey) && e.key === "Enter") onSubmit(); }}
      />

      {/* Recipient + submit row */}
      <div className="input-row">
        <select
          className="select"
          value={recipient}
          onChange={(e) => onRecipientChange(e.target.value)}
        >
          {RECIPIENTS.map((r) => (
            <option key={r.value} value={r.value}>{r.label}</option>
          ))}
        </select>

        <button
          className="submit-btn"
          onClick={onSubmit}
          disabled={loading || !message.trim()}
        >
          {loading ? "変換中…" : "Generate ✦"}
        </button>
      </div>
    </div>
  );
}
