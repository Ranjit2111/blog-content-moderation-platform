@echo off
echo Starting backend...
start "backend" cmd /k "call env\Scripts\activate && uvicorn app.main:app --reload"
timeout /t 5 /nobreak >nul
echo Starting frontend...
cd frontend
start "frontend" cmd /k "npm run dev"
echo Application started! 