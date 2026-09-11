@echo off
echo Starting Todo App (Backend + Frontend)...
start "Todo Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\python.exe main.py"
start "Todo Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
echo Both servers launched in separate windows!
echo Frontend will be at: http://localhost:5173
echo Backend will be at:  http://127.0.0.1:8000
