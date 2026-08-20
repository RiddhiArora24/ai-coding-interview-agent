Write-Host ""
Write-Host "Starting AI Coding Interview Backend..." -ForegroundColor Cyan
Write-Host ""
Write-Host "API:  http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Docs: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host ""

& ".\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload
