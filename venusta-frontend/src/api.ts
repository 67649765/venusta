// 本地开发时自动使用直接API地址，构建时使用.env配置
// 这样在本地开发时(npm run dev)不需要重启容器就能访问API
const BASE = import.meta.env.DEV 
  ? 'http://localhost:8000'  // 本地开发直接连API服务
  : (import.meta.env.VITE_API_BASE as string);  // 构建时使用.env配置

export async function genExam() {
  const body = {
    grade: "junior",
    subject: "math",
    chapter: "quadratic",
    knowledge_points: ["graph_properties"],
    item_type_ratio: { single_choice: 1, subjective: 1 },
    difficulty: 3,
    num_items: 2,
  };
  const r = await fetch(`${BASE}/exams/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error("generate failed");
  return r.json();
}

export async function grade(paper_id: number, item_id: number) {
  const r = await fetch(`${BASE}/grading/grade`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: 1,
      paper_id,
      item_id,
      answer: "2",
      steps: ["axis", "vertex"],
    }),
  });
  if (!r.ok) throw new Error("grade failed");
  return r.json();
}

export async function dashboard() {
  const r = await fetch(`${BASE}/dashboard/metrics`);
  if (!r.ok) throw new Error("dashboard failed");
  return r.json();
}