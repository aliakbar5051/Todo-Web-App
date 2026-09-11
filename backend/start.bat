@echo off
title Todo App - Backend
cd /d "%~dp0"
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe main.py
) else (
    echo [ERROR] Virtual environment not found in backend\venv!
    pause
)
