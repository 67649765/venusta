[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Continue"

Write-Host "===== Simple API Test ====="

# Test Health Check
Write-Host "`n1. Testing Health Check..."
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
    Write-Host "✅ Health check successful: $($health.status)"
} catch {
    Write-Host "❌ Health check failed: $_"
}

# Test Dashboard Metrics
Write-Host "`n2. Testing Dashboard Metrics..."
try {
    $dashboard = Invoke-RestMethod -Uri "http://localhost:8000/dashboard/metrics" -Method GET
    Write-Host "✅ Dashboard metrics successful:"
    Write-Host "   Responses: $($dashboard.responses)"
    Write-Host "   Kappa: $($dashboard.kappa)"
    Write-Host "   MAE: $($dashboard.mae)"
} catch {
    Write-Host "❌ Dashboard metrics failed: $_"
}

# Test Exam Generation
Write-Host "`n3. Testing Exam Generation..."
try {
    $jsonBody = '{"grade":"junior","subject":"math","chapter":"quadratic","knowledge_points":["graph_properties"],"item_type_ratio":{"single_choice":1,"subjective":1},"difficulty":3,"num_items":2}'
    $generate = Invoke-RestMethod -Uri "http://localhost:8000/exams/generate" -Method POST -ContentType "application/json" -Body $jsonBody
    Write-Host "✅ Exam generation successful:" -ForegroundColor Green
    Write-Host "   Paper ID: $($generate.paper_id)"
    Write-Host "   Item IDs: $($generate.item_ids -join ", ")"
} catch {
    Write-Host "❌ Exam generation failed: $_"
}

Write-Host "`n===== Test Completed ====="