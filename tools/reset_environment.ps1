[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "SilentlyContinue"

Write-Host "=== Resetting VenusTA Environment ==="

# 停止并移除所有容器和卷
Write-Host "Stopping and removing containers..."
docker compose down -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Docker compose down failed, continuing with local reset"
}

# 清理本地缓存和临时文件
Write-Host "Cleaning local cache and temporary files..."
if (Test-Path "api/app/__pycache__") {
    Remove-Item -Recurse -Force "api/app/__pycache__"
}
if (Test-Path "api/app/tests/__pycache__") {
    Remove-Item -Recurse -Force "api/app/tests/__pycache__"
}

# 重建并启动服务
Write-Host "Rebuilding and starting services..."
docker compose up -d --build
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Services rebuilt and started successfully"
    
    # 等待服务启动
    Write-Host "Waiting for services to initialize..."
    Start-Sleep -Seconds 10
    
    # 运行full_loop测试
    Write-Host "Running full loop test..."
    powershell -ExecutionPolicy Bypass -File .\tools\full_loop.ps1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Full loop test completed successfully!"
    } else {
        Write-Host "❌ Full loop test failed"
    }
} else {
    Write-Host "❌ Docker compose up failed"
}

Write-Host "=== Reset Complete ==="