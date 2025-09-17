[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

function post($url, $obj) {
  $json = $obj | ConvertTo-Json -Depth 8
  return Invoke-RestMethod -Uri $url -Method POST -ContentType "application/json; charset=utf-8" -Body $json
}

function printResult($step, $result) {
  Write-Host "`n$step Result:`"
  $result | ConvertTo-Json -Depth 5 | Write-Output
}

Write-Host "===== VenusTA Complete Test Suite ====="

# 1. Generate Exam Paper
Write-Host "`n1. Generating Exam Paper..."
try {
    $generateResponse = post "http://localhost:8000/exams/generate" @{
      grade="junior";
      subject="math";
      chapter="quadratic";
      knowledge_points=@("graph_properties");
      item_type_ratio=@{ single_choice=1; subjective=1 };
      difficulty=3;
      num_items=2
    }
    printResult "Exam Generation" $generateResponse
    $paperId = $generateResponse.paper_id
    $itemIds = $generateResponse.item_ids
} catch {
    Write-Host "❌ Exam generation failed: $_"
    exit 1
}

# 2. Health Check
Write-Host "`n2. Performing Health Check..."
try {
    $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
    printResult "Health Check" $healthResponse
} catch {
    Write-Host "❌ Health check failed: $_"
}

# 3. Grading
Write-Host "`n3. Submitting Answers for Grading..."
try {
    if ($itemIds.Count -gt 0) {
        $firstItemId = $itemIds[0]
        $gradeResponse = post "http://localhost:8000/grading/grade" @{
          user_id=1;
          paper_id=$paperId;
          item_id=$firstItemId;
          answer="2";
          steps=@("axis_of_symmetry","vertex_calculation")
        }
        printResult "Grading" $gradeResponse
    }
} catch {
    Write-Host "❌ Grading failed: $_"
}

# 4. Diagnosis
Write-Host "`n4. Generating Diagnosis..."
try {
    $diagnosisResponse = post "http://localhost:8000/diagnosis" @{
      user_id=1;
      paper_id=$paperId
    }
    printResult "Diagnosis" $diagnosisResponse
} catch {
    Write-Host "❌ Diagnosis failed: $_"
}

# 5. Review
Write-Host "`n5. Generating Review..."
try {
    $reviewResponse = post "http://localhost:8000/review" @{
      user_id=1;
      paper_id=$paperId
    }
    printResult "Review" $reviewResponse
} catch {
    Write-Host "❌ Review generation failed: $_"
}

# 6. Dashboard Metrics
Write-Host "`n6. Fetching Dashboard Metrics..."
try {
    $dashboardResponse = Invoke-RestMethod -Uri "http://localhost:8000/dashboard/metrics" -Method GET
    printResult "Dashboard Metrics" $dashboardResponse
} catch {
    Write-Host "❌ Dashboard metrics fetch failed: $_"
}

Write-Host "`n===== Test Completed ====="