@echo off
curl -X POST http://localhost:8000/exams/generate -H "Content-Type: application/json" --data-binary @exam_request.json