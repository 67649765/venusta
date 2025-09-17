from fastapi import APIRouter
from ..schemas import DiagnoseIn, DiagnoseOut
from .. import db
from typing import Dict, Any
import json

router = APIRouter()

@router.post("", response_model=DiagnoseOut)
def run_diagnosis(in_: DiagnoseIn):
    # 简化：统计该试卷该学生的得分分布，返回占位热力/错因
    rows = db.fetchall("SELECT r.score, i.knowledge_points FROM responses r JOIN items i ON r.item_id=i.id WHERE r.user_id=%s AND r.paper_id=%s", (in_.user_id, in_.paper_id))
    heatmap: Dict[str, float] = {}
    for r in rows:
        for kp in (r["knowledge_points"] or []):
            heatmap[kp] = max(heatmap.get(kp, 0.0), float(r["score"] or 0.0))
    error_dist = {"单位错": 0.3, "步骤漏": 0.4, "概念混淆": 0.3}
    rec = {"基础题": [1,2], "变式题": [3]}
    db.execute("INSERT INTO diagnosis (user_id, paper_id, heatmap, error_dist, recommendations) VALUES (%s,%s,%s,%s,%s)", (in_.user_id, in_.paper_id, json.dumps(heatmap), json.dumps(error_dist), json.dumps(rec)))
    return {"heatmap": heatmap, "error_dist": error_dist, "recommendations": rec}
