[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

function post($url, $obj) {
  $json = $obj | ConvertTo-Json -Depth 8
  return Invoke-RestMethod -Uri $url -Method POST -ContentType "application/json; charset=utf-8" -Body $json
}

Write-Host "1. Generating exam paper..."
$gen = post "http://localhost:8000/exams/generate" @{
  grade="junior"; subject="math"; chapter="quadratic"; 
  knowledge_points=@("graph_properties");
  item_type_ratio=@{ single_choice=1; subjective=1 };
  difficulty=3; num_items=2
}
$paper = $gen.paper_id
$item = $gen.item_ids[0]
$gen | ConvertTo-Json -Depth 5 | Write-Output

Write-Host "`n2. Health check..."
$health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
$health | ConvertTo-Json -Depth 5 | Write-Output

Write-Host "`n3. Dashboard metrics..."
$dash = Invoke-RestMethod -Uri "http://localhost:8000/dashboard/metrics" -Method GET
$dash | ConvertTo-Json -Depth 5 | Write-Output