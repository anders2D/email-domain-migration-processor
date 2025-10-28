@echo off
REM Script wrapper para ejecutar publish_with_timestamp.py en Windows

cd /d "%~dp0\.."
python scripts\publish_with_timestamp.py
pause
