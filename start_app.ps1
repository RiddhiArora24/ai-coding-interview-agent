$root = $PSScriptRoot

Write-Host ""
Write-Host "Starting AI Coding Interview Agent..." -ForegroundColor Cyan
Write-Host ""

Start-Process powershell `
    -WorkingDirectory $root `
    -ArgumentList @(
        "-NoExit",
        "-Command",
        ".\.venv\Scripts\python.exe -m uvicorn app.main:app --reload"
    )

Start-Sleep -Seconds 3

Start-Process powershell `
    -WorkingDirectory "$root\frontend" `
    -ArgumentList @(
        "-NoExit",
        "-Command",
        "npm run dev"
    )

Write-Host "Backend:  http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host ""
