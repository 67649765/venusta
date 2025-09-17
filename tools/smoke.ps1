[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

Write-Host "Running smoke tests inside venusta-api container..."

# 在容器内运行 pytest 冒烟测试
docker exec -it venusta-api bash -lc "pytest -q /app/app/tests/test_smoke.py"