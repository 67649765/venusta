from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class Item(BaseModel):
    id: int
    stem: str
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    solution: Optional[str] = None
    difficulty: Optional[int] = None
    knowledge_points: Optional[List[str]] = None
    item_type: Optional[str] = None

class PaperCreate(BaseModel):
    title: str
    item_ids: List[int]

class PaperOut(BaseModel):
    paper_id: int
    item_ids: List[int]

class GradeIn(BaseModel):
    user_id: int
    paper_id: int
    item_id: int
    answer: str
    steps: Optional[List[str]] = None

class GradeOut(BaseModel):
    score: float
    judge_meta: Dict[str, Any]

class DiagnoseIn(BaseModel):
    user_id: int
    paper_id: int

class DiagnoseOut(BaseModel):
    heatmap: Dict[str, float]
    error_dist: Dict[str, float]
    recommendations: Dict[str, Any]
