from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import exams, grading, diagnosis, review, dashboard

app = FastAPI(title="VenusTA | AI 智能助教", version="0.1.0")

# CORS：允许 Vite 开发服务器访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(exams.router, prefix="/exams", tags=["出题器"])
app.include_router(grading.router, prefix="/grading", tags=["评分器"])
app.include_router(diagnosis.router, prefix="/diagnosis", tags=["诊断器"])
app.include_router(review.router, prefix="/review", tags=["讲评与复练"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["看板"])
