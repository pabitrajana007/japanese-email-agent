const SCENARIOS = [
  { label: "Meeting request", text: "Can we move tomorrow's meeting to 3pm?" },
  { label: "Deadline extension", text: "I need 2 more days to finish the report, is that okay?" },
  { label: "Thank you", text: "Thanks for your help with the project last week." },
  { label: "Apology", text: "Sorry for the delay in my response." },
  { label: "Follow up", text: "Just checking in on the proposal I sent last week." },
];

interface Props {
  onSelect: (text: string) => void;
}

export function ScenarioChips({ onSelect }: Props) {
  return (
    <div className="scenarios">
      <p className="section-label">QUICK START</p>
      <div className="chip-row">
        {SCENARIOS.map((s) => (
          <button key={s.label} className="chip" onClick={() => onSelect(s.text)}>
            {s.label}
          </button>
        ))}
      </div>
    </div>
  );
}
