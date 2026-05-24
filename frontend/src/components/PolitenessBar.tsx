interface Props {
  level: number; // 1-5
}

export function PolitenessBar({ level }: Props) {
  return (
    <div className="politeness-row">
      <span className="section-label">POLITENESS</span>
      <div className="pip-row">
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className={`pip ${i <= level ? "pip--filled" : ""}`} />
        ))}
      </div>
    </div>
  );
}
