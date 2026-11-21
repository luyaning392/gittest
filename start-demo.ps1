$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$python = Join-Path $root ".venv\Scripts\python.exe"
$backendArgs = "-m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000"
$frontendArgs = "-m http.server 5500 --directory `"$root`""

Write-Host "正在启动银发守护演示..." -ForegroundColor Cyan

Start-Process -FilePath $python -ArgumentList $backendArgs -WorkingDirectory $root
Start-Process -FilePath $python -ArgumentList $frontendArgs -WorkingDirectory $root

Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:5500/index.html"

Write-Host "前端：http://127.0.0.1:5500/index.html" -ForegroundColor Green
Write-Host "后端：http://127.0.0.1:8000/api/health" -ForegroundColor Green
Write-Host "演示脚本请见 DEMO.md" -ForegroundColor Cyan
