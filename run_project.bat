@echo off
title VERITRACE AI Launcher

cd /d "%~dp0"

echo =====================================
echo      VERITRACE AI Starting...
echo =====================================
echo.

REM Create virtual environment if missing
if not exist backend\venv_new (
    echo Creating virtual environment...
    python -m venv backend\venv_new
)

REM Install dependencies
call backend\venv_new\Scripts\activate.bat
echo Installing dependencies (first run only)...
pip install -r requirements.txt

REM Start Backend
start "Backend" cmd /k "cd backend && call venv_new\Scripts\activate.bat && python -m uvicorn main:app --host 127.0.0.1 --port 8000"

REM Wait for backend
timeout /t 5 >nul

REM Start Frontend
start "Frontend" cmd /k "cd frontend && python -m http.server 8001"

REM Open Browser
timeout /t 2 >nul
start http://127.0.0.1:8001/index.html