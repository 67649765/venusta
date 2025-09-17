import { useState } from "react";
import { genExam, grade, dashboard } from "./api";

export default function App() {
  const [paperId, setPaperId] = useState<number>();
  const [itemId, setItemId] = useState<number>();
  const [score, setScore] = useState<number>();
  const [dash, setDash] = useState<any>();

  const doGen = async () => {
    const data = await genExam();
    setPaperId(data.paper_id);
    setItemId(data.item_ids?.[0]);
  };

  const doGrade = async () => {
    if (!paperId || !itemId) return;
    const g = await grade(paperId, itemId);
    setScore(g.score);
  };

  const doDash = async () => {
    const d = await dashboard();
    setDash(d);
  };

  return (
    <div style={{ fontFamily: "ui-sans-serif", padding: 24, maxWidth: 720 }}>
      <h1>VenusTA · Teacher Console (mini)</h1>
      <div style={{ display: "grid", gap: 12 }}>
        <button onClick={doGen}>1) Generate Exam</button>
        <div>paper_id: {paperId?.toString() ?? "-"}</div>
        <div>item_id: {itemId?.toString() ?? "-"}</div>

        <button onClick={doGrade} disabled={!paperId || !itemId}>
          2) Grade First Item (answer="2")
        </button>
        <div>score: {score ?? "-"}</div>

        <button onClick={doDash}>3) Dashboard</button>
        <pre style={{ background: "#f6f8fa", padding: 12, borderRadius: 8 }}>
{dash ? JSON.stringify(dash, null, 2) : "// click Dashboard"}
        </pre>
      </div>
    </div>
  );
}