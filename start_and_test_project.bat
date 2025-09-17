@echo off

REM 检查Docker服务是否运行
powershell -Command "& {
    $dockerService = Get-Service *docker* -ErrorAction SilentlyContinue
    if (-not $dockerService -or $dockerService.Status -ne 'Running') {
        Write-Host 'Docker服务未运行，正在尝试启动...'
        try {
            Start-Service com.docker.service -ErrorAction Stop
            Write-Host 'Docker服务启动成功'
        } catch {
            Write-Host '错误：无法启动Docker服务，请以管理员身份运行Docker Desktop'
            pause
            exit 1
        }
    } else {
        Write-Host 'Docker服务已在运行'
    }
}"

REM 启动项目服务
cd /d d:\AI1111\venus-ta-starter\services
Write-Host '正在启动Docker容器服务...'
docker compose up -d --build

REM 等待服务启动
Write-Host '等待服务启动中（10秒）...'
timeout /t 10 /nobreak >nul

REM 显示容器状态
Write-Host '\n===== 容器状态 ====='
docker compose ps

REM 测试API连接
Write-Host '\n===== API连接测试 ====='
powershell -Command "& {
    try {
        $response = Invoke-RestMethod -Uri 'http://localhost/api/health' -Method GET -UseBasicParsing
        Write-Host 'API健康检查成功: ' $response
    } catch {
        Write-Host '错误：API健康检查失败，请检查容器日志'
    }
}"

REM 运行完整测试（可选）
:choice
set /p choice=是否运行完整API测试？(y/n): 
if /i "%choice%"=="y" goto run_test
if /i "%choice%"=="n" goto end
goto choice

:run_test
Write-Host '\n===== 开始运行完整API测试 ====='
powershell -ExecutionPolicy Bypass -File .\tools\full_loop.ps1

:end
Write-Host '\n项目启动完成！您可以通过以下地址访问：'
Write-Host '前端页面: http://localhost'
Write-Host 'API健康检查: http://localhost/api/health'
pause