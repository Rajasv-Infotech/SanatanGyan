@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo Cleaning old Visual Studio / MAUI build output...
if exist "SanatanGyan\bin" rmdir /s /q "SanatanGyan\bin"
if exist "SanatanGyan\obj" rmdir /s /q "SanatanGyan\obj"
echo Done. Open SanatanGyan.sln and press F5 with Windows Machine selected.
pause
