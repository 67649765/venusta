[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

function Write-StepHeader($title) {
    Write-Host "`n=================================================="
    Write-Host "🔹 $title"
    Write-Host "=================================================="
}

function Write-Success($message) {
    Write-Host "✅ $message"
}

function Handle-Error($stepName, $message, $containerName) {
    Write-Host "`n❌ ERROR during $stepName: $message"
    Write-Host "   建议查看容器日志：docker logs $containerName"
    Write-Host "   或使用命令：docker compose logs $containerName -f"
    exit 1
}

function post($url, $obj) {
    try {
        $json = $obj | ConvertTo-Json -Depth 8
        Invoke-RestMethod -Uri $url -Method POST -ContentType "application/json" -Body $json -TimeoutSec 30
    } catch {
        $errorMessage = $_.Exception.Message
        if ($errorMessage -like "*Unable to connect*" -or $errorMessage -like "*Could not resolve*" -or $errorMessage -like "*No connection could be made*") {
            Handle-Error "API 连接" $errorMessage "venusta-frontend"
        } else {
            Handle-Error "API 请求" $errorMessage "venusta-api"
        }
    }
}

function get($url) {
    try {
        Invoke-RestMethod -Uri $url -Method GET -TimeoutSec 30
    } catch {
        $errorMessage = $_.Exception.Message
        if ($errorMessage -like "*Unable to connect*" -or $errorMessage -like "*Could not resolve*" -or $errorMessage -like "*No connection could be made*") {
            Handle-Error "API 连接" $errorMessage "venusta-frontend"
        } else {
            Handle-Error "API 请求" $errorMessage "venusta-api"
        }
    }
}

# 1) 生成试卷 (出题)
Write-StepHeader "1️⃣ 生成试卷 (出题)"
try {
    $generateResponse = post "http://localhost/api/exams/generate" @{
        grade="junior"
        subject="math"
        chapter="quadratic"
        knowledge_points=@("graph_properties")
        item_type_ratio=@{ single_choice=1; subjective=1 }
        difficulty=3
        num_items=2
    }
    $paperId = $generateResponse.paper_id
    $firstItemId = $generateResponse.item_ids[0]
    Write-Success "试卷生成成功: paper=$paperId, first_item=$firstItemId"
} catch {
    Handle-Error "生成试卷" "无法生成试卷，可能是数据库连接问题或API服务异常" "venusta-api"
}

# 2) 评分答案 (批改)
Write-StepHeader "2️⃣ 评分答案 (批改)"
try {
    $gradeResponse = post "http://localhost/api/grading/grade" @{
        user_id=1
        paper_id=$paperId
        item_id=$firstItemId
        answer="2"
        steps=@("axis","vertex")
    }
    Write-Success "答案评分完成: score=$($gradeResponse.score)"
} catch {
    Handle-Error "答案评分" "无法完成评分，可能是答案格式错误或评分服务异常" "venusta-api"
}

# 3) 诊断分析 (诊断)
Write-StepHeader "3️⃣ 诊断分析 (诊断)"
try {
    $diagnosisResponse = post "http://localhost/api/diagnosis" @{
        user_id=1
        paper_id=$paperId
    }
    Write-Success "诊断分析完成"
} catch {
    Handle-Error "诊断分析" "无法完成诊断分析，可能是诊断服务异常" "venusta-api"
}

# 4) 生成讲评 (讲评)
Write-StepHeader "4️⃣ 生成讲评 (讲评)"
try {
    $reviewResponse = post "http://localhost/api/review" @{
        user_id=1
        paper_id=$paperId
    }
    Write-Success "讲评生成完成"
} catch {
    Handle-Error "生成讲评" "无法生成讲评，可能是讲评服务异常" "venusta-api"
}

# 5) 获取仪表板数据 (看板)
Write-StepHeader "5️⃣ 获取仪表板数据 (看板)"
try {
    $dashboardResponse = get "http://localhost/api/dashboard/metrics"
    Write-Success "仪表板数据获取完成: responses=$($dashboardResponse.responses); kappa=$($dashboardResponse.kappa); mae=$($dashboardResponse.mae)"
} catch {
    Handle-Error "获取仪表板数据" "无法获取仪表板数据，可能是数据分析服务异常" "venusta-api"
}

# 全部测试完成
Write-Host "`n=================================================="
Write-Host "🎉 恭喜！Full loop 测试已成功完成！"
Write-Host "==================================================
"