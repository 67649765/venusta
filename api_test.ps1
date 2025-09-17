[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

Write-Host "Testing API connectivity..."

# Test basic connection
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
    Write-Host "Health check successful: $($health.status)"
} catch {
    Write-Host "Connection failed: Cannot access API service"
    exit 1
}

# Check dashboard data
try {
    $dashboard = Invoke-RestMethod -Uri "http://localhost:8000/dashboard/metrics" -Method GET
    Write-Host "Dashboard data:"
    Write-Host "   Responses count: $($dashboard.responses)"
    Write-Host "   Kappa: $($dashboard.kappa)"
    Write-Host "   MAE: $($dashboard.mae)"
} catch {
    Write-Host "Failed to get dashboard data"
}