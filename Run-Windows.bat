@echo off
setlocal
cd /d "%~dp0"
title Sanatan Gyan - Windows Build Check
set "PROJECT=%~dp0SanatanGyan\SanatanGyan.csproj"
set "TFM=net10.0-windows10.0.19041.0"

echo This file is OPTIONAL in v0.8.0.
echo Visual Studio should run directly from a fresh extract:
echo   SanatanGyan.sln ^> Windows Machine ^> F5

echo.
echo Running only a build check...
rem Full restore is intentional: it keeps BOTH Android and Windows in project.assets.json.
dotnet restore "%PROJECT%" || goto :failed
dotnet build "%PROJECT%" -f %TFM% -c Debug -p:Platform=x64 --no-restore || goto :failed

echo.
echo Windows build check succeeded.
pause
exit /b 0

:failed
echo.
echo Windows build check failed. Read the first error above.
pause
exit /b 1
