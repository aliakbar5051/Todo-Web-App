@echo off
title Todo App - Backend
echo ===================================
echo Starting FastAPI Backend Server...
echo ===================================
cd /d "%~dp0backend"
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe main.py
) else (
    echo [ERROR] Python virtual environment not found in backend\venv!
    echo Please create it by running:
    echo   cd backend
    echo   python -m venv venv
    echo   venv\Scripts\pip install -r requirements.txt
    pause
)
