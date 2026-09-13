@echo off
setlocal EnableExtensions
cd /d "%~dp0"

where py >nul 2>&1
if not errorlevel 1 (
    py tools\validate_project.py
    pause
    exit /b %errorlevel%
)

where python >nul 2>&1
if not errorlevel 1 (
    python tools\validate_project.py
    pause
    exit /b %errorlevel%
)

echo Python is not installed. Validation is optional; Visual Studio build is the final compile check.
pause
exit /b 1
