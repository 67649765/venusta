[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

# Function to make POST requests
function Post-Request($url, $body) {
    $json = $body | ConvertTo-Json -Depth 8
    try {
        return Invoke-RestMethod -Uri $url -Method POST -ContentType "application/json" -Body $json
    } catch {
        Write-Host "Error at $url: $_"
        exit 1
    }
}

# 1. Generate Exam Paper
Write-Host "1. Generating Exam Paper..."
$genBody = @{
    grade="junior_high";
    subject="math";
    chapter="quadratic_function";
    knowledge_points=@("graph_properties");
    item_type_ratio=@{ single_choice=1; subjective=1 };
    difficulty=3;
    num_items=2
}
$genResponse = Post-Request "http://localhost:8000/exams/generate" $genBody
Write-Host "Paper ID: $($genResponse.paper_id)"
Write-Host "Item IDs: $($genResponse.item_ids -join ', ')"

if (-not $genResponse.paper_id) {
    Write-Host "Failed to generate paper"
    exit 1
}

# 2. Grade an answer
Write-Host "\n2. Grading Answer..."
$gradeBody = @{
    user_id=1;
    paper_id=$genResponse.paper_id;
    item_id=$genResponse.item_ids[0];
    answer="2";
    steps=@("symmetry_axis","vertex_method")
}
$gradeResponse = Post-Request "http://localhost:8000/grading/grade" $gradeBody
Write-Host "Score: $($gradeResponse.score)"

# 3. Check dashboard metrics
Write-Host "\n3. Getting Dashboard Metrics..."
try {
    $dashResponse = Invoke-RestMethod -Uri "http://localhost:8000/dashboard/metrics" -Method GET
    Write-Host "Responses Count: $($dashResponse.responses)"
    Write-Host "Kappa: $($dashResponse.kappa)"
    Write-Host "MAE: $($dashResponse.mae)"
} catch {
    Write-Host "Error getting dashboard metrics: $_"
}