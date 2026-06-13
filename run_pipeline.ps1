$ErrorActionPreference = "Stop"
$env:PYTHONUNBUFFERED = "1"

$ProjectRoot = "D:\egg_price_procject"
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$Scripts = @(
    "data_scrap\egg_scraper.py",
    "data_scrap\festival_generator.py",
    "data_scrap\weather_scraper.py",
    "analysis\feature_extraction.py"
)

Write-Host "====================================="
Write-Host "Starting Egg Price Data Pipeline"
Write-Host "====================================="
Write-Host ""

foreach ($Script in $Scripts) {
    $ScriptPath = Join-Path $ProjectRoot $Script
    Write-Host "Running $Script"
    & $Python -u $ScriptPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "====================================="
        Write-Host "PIPELINE FAILED"
        Write-Host "====================================="
        exit $LASTEXITCODE
    }
}

Write-Host ""
Write-Host "====================================="
Write-Host "ALL SCRIPTS COMPLETED SUCCESSFULLY"
Write-Host "====================================="
