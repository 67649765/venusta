[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 检查API服务状态
Write-Host "=== API Status Check ==="
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5
    Write-Host "✅ API Health: $($health.status)"
} catch {
    Write-Host "❌ API service check failed"
}

# 获取仪表板指标
try {
    $metrics = Invoke-RestMethod -Uri "http://localhost:8000/dashboard/metrics" -Method GET -TimeoutSec 5
    Write-Host "✅ Dashboard: responses=$($metrics.responses), kappa=$($metrics.kappa), mae=$($metrics.mae)"
} catch {
    Write-Host "❌ Dashboard check failed"
}

Write-Host "=== Check Complete ==="