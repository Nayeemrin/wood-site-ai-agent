@echo off
title Wood-Site AI Agent Launcher

cd /d "%~dp0"

echo Starting Wood-Site AI Agent...
echo.

start "Wood-Site AI Agent Server" ".venv-agent\Scripts\python.exe" -m streamlit run "src\dashboard.py"

echo Waiting for the dashboard to start...
timeout /t 4 /nobreak >nul

start "" "http://localhost:8501"

exit