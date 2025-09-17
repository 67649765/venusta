from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ReviewIn(BaseModel):
    user_id: int
    paper_id: int

@router.post("", summary="生成讲评与复练（占位）")
def generate_review(_in: ReviewIn):
    # 占位：真实实现应做证据检索 + 模板化提示
    return {
        "summary": "三步法：标错→析因→补练",
        "cards": [
            {"type": "标错", "content": "第3题：单位换算错误"},
            {"type": "析因", "content": "忽视题干单位，未统一量纲"},
            {"type": "补练", "content": "做 2 道单位换算基础题 + 1 道变式题"}
        ]
    }
