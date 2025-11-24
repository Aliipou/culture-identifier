@echo off
echo ================================================================================
echo Cultural Personality Analyzer - Startup Script
echo ================================================================================
echo.

echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 8 /nobreak > nul

echo [2/2] Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 3000"
timeout /t 3 /nobreak > nul

echo.
echo ================================================================================
echo System is starting...
echo ================================================================================
echo.
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend UI: http://localhost:3000
echo.
echo Press any key to open the frontend in your browser...
pause > nul

start http://localhost:3000
