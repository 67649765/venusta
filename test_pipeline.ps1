# Ensure Chinese JSON is not garbled
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

function post($url, $obj) {
  $json = $obj | ConvertTo-Json -Depth 8
  return Invoke-RestMethod -Uri $url -Method POST -ContentType "application/json; charset=utf-8" -Body $json
}

Write-Host "① Generating exam paper..."
$gen = post "http://localhost:8000/exams/generate" @{
  grade="初中"; subject="数学"; chapter="二次函数";
  knowledge_points=@("图像性质");
  item_type_ratio=@{ single_choice=1; subjective=1 };
  difficulty=3; num_items=2
}
$paper = $gen.paper_id
$item = $gen.item_ids[0]
$gen | ConvertTo-Json -Depth 5 | Write-Output

Write-Host "`n② Grading..."
$grade = post "http://localhost:8000/grading/grade" @{
  user_id=1; paper_id=$paper; item_id=$item; answer="2";
  steps=@("对称轴","顶点求法")
}
$grade | ConvertTo-Json -Depth 5 | Write-Output

Write-Host "`n③ Diagnosing..."
$diag = post "http://localhost:8000/diagnosis" @{ user_id=1; paper_id=$paper }
$diag | ConvertTo-Json -Depth 5 | Write-Output

Write-Host "`n④ Reviewing..."
$rev = post "http://localhost:8000/review" @{ user_id=1; paper_id=$paper }
$rev | ConvertTo-Json -Depth 5 | Write-Output

Write-Host "`n⑤ Dashboard..."
$dash = Invoke-RestMethod -Uri "http://localhost:8000/dashboard/metrics" -Method GET
$dash | ConvertTo-Json -Depth 5 | Write-Output