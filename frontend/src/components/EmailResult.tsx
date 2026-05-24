import { useState } from "react";
import type { EmailResponse } from "../api";

type Tab = "formal" | "keigo" | "sonkeigo";

const TABS: { key: Tab; label: string }[] = [
  { key: "formal",   label: "Formal 丁寧語" },
  { key: "keigo",    label: "Keigo 敬語" },
  { key: "sonkeigo", label: "Sonkeigo 尊敬語" },
];

interface Props {
  result: EmailResponse;
}

export function EmailResult({ result }: Props) {
  const [tab, setTab] = useState<Tab>("formal");
  const [copied, setCopied] = useState("");

  const variant = result[tab];

  function copy(text: string, key: string) {
    navigator.clipboard.writeText(text);
    setCopied(key);
    setTimeout(() => setCopied(""), 2000);
  }

  return (
    <div className="result">
      {/* Cultural tip */}
      <div className="tip">
        <span className="tip-label">💡 Cultural tip</span>
        <p>{result.cultural_tip}</p>
      </div>

      {/* Tabs */}
      <div className="tabs">
        {TABS.map((t) => (
          <button
            key={t.key}
            className={`tab ${tab === t.key ? "tab--active" : ""}`}
            onClick={() => setTab(t.key)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Politeness level */}
      <div className="politeness">
        <span className="field-label">Politeness</span>
        <div className="pips">
          {[1,2,3,4,5].map((i) => (
            <div key={i} className={`pip ${i <= variant.politeness_level ? "pip--on" : ""}`} />
          ))}
        </div>
      </div>

      {/* Subject */}
      <div className="field">
        <div className="field-header">
          <span className="field-label">件名 Subject</span>
          <button className="copy-btn" onClick={() => copy(variant.subject, "subj")}>
            {copied === "subj" ? "✓ Copied" : "Copy"}
          </button>
        </div>
        <div className="field-value jp">{variant.subject}</div>
      </div>

      {/* Body */}
      <div className="field">
        <div className="field-header">
          <span className="field-label">本文 Body</span>
          <button className="copy-btn" onClick={() => copy(variant.body, "body")}>
            {copied === "body" ? "✓ Copied" : "Copy"}
          </button>
        </div>
        <div className="field-value jp body">{variant.body}</div>
      </div>

      {/* Explanation */}
      <div className="field">
        <span className="field-label">解説 Explanation</span>
        <p className="explanation">{variant.explanation}</p>
      </div>

      {/* Copy all */}
      <button
        className="copy-all"
        onClick={() => copy(`件名: ${variant.subject}\n\n${variant.body}`, "all")}
      >
        {copied === "all" ? "✓ Copied!" : "Copy full email"}
      </button>
    </div>
  );
}
