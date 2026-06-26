@echo off
echo =======================================================
echo    IoT Vulnerability Scanner - Startup Script
echo =======================================================
echo.

echo [1/3] Starting Python Backend API (FastAPI) on port 8000...
start "Backend API" cmd /k "cd backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000"

echo [2/3] Starting Virtual IoT Scanner Engine (Background Service)...
:: We add a 3-second timeout so the API has time to start first
start "Virtual IoT Scanner" cmd /k "timeout /t 3 >nul && cd backend && python background_service.py"

echo [3/3] Starting React Frontend Dashboard (Vite)...
start "Frontend Dashboard" cmd /k "cd frontend && npm run dev"

echo.
echo All services are launching in separate windows!
echo Waiting a few seconds for the frontend server to initialize...
timeout /t 5 /nobreak >nul
echo Opening your default web browser to the dashboard...
start http://localhost:5173
echo.
echo If the browser didn't open, manually go to: http://localhost:5173
pause
