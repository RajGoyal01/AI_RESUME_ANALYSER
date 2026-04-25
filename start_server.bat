@echo off
echo ================================================
echo   AI Resume Analyser - Starting Backend Server
echo ================================================
echo.
echo Server will start on http://localhost:5000
echo You can also use VS Code "Go Live" to view the frontend
echo.
cd /d "%~dp0backend"
python app.py
pause
