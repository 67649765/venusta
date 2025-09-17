[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

Write-Host "测试系统API连接..."

# 测试基本连接
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
    Write-Host "✅ 健康检查成功: $($health.status)"
} catch {
    Write-Host "❌ 连接失败: 无法访问API服务"
    exit 1
}

# 查看仪表板数据
try {
    $dashboard = Invoke-RestMethod -Uri "http://localhost:8000/dashboard/metrics" -Method GET
    Write-Host "✅ 仪表板数据:"
    Write-Host "   响应数量: $($dashboard.responses)"
    Write-Host "   Kappa系数: $($dashboard.kappa)"
    Write-Host "   MAE值: $($dashboard.mae)"
} catch {
    Write-Host "❌ 获取仪表板数据失败"
}