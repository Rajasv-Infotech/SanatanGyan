@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title Sanatan Gyan - Build Android APK

set "PROJECT=%~dp0SanatanGyan\SanatanGyan.csproj"
set "PROJECTDIR=%~dp0SanatanGyan"
set "TFM=net10.0-android"
set "OUTDIR=%~dp0artifacts\android"
set "FINALAPK=%OUTDIR%\SanatanGyan-v0.8.1-LocalTest.apk"
set "ANDROIDBIN=%PROJECTDIR%\bin\Release\%TFM%"
set "MANIFEST=%PROJECTDIR%\Platforms\Android\AndroidManifest.xml"

echo ============================================================
echo   SANATAN GYAN v0.8.1 - ANDROID APK BUILDER
echo ============================================================
echo.

where dotnet >nul 2>&1 || goto :no_dotnet
if not exist "%PROJECT%" goto :missing_project
if not exist "%MANIFEST%" goto :missing_manifest

if not exist "%OUTDIR%" mkdir "%OUTDIR%"
if exist "%FINALAPK%" del /q "%FINALAPK%"
if exist "%PROJECTDIR%\obj\Release\%TFM%" rmdir /s /q "%PROJECTDIR%\obj\Release\%TFM%"
if exist "%PROJECTDIR%\bin\Release\%TFM%" rmdir /s /q "%PROJECTDIR%\bin\Release\%TFM%"

echo [1/4] Restoring MAUI workloads...
dotnet workload restore "%PROJECT%"
if errorlevel 1 goto :failed

echo.
echo [2/4] Restoring ALL project target frameworks...
rem IMPORTANT: do not restore only net10.0-android here.
rem A target-specific restore overwrites obj\project.assets.json and then Visual Studio
rem reports NETSDK1005 for the Windows target. Full restore keeps Android + Windows assets.
dotnet restore "%PROJECT%"
if errorlevel 1 goto :failed

echo.
echo [3/4] Creating signed standalone APK...
rem MAUI finds Platforms\Android\AndroidManifest.xml automatically.
rem Do not pass or override AndroidManifest on the command line.
dotnet build "%PROJECT%" -f %TFM% -c Release -p:Platform=AnyCPU -t:SignAndroidPackage -p:AndroidPackageFormats=apk -p:AndroidKeyStore=false -p:AndroidUseApkSigner=true --no-restore
if errorlevel 1 goto :failed

echo.
echo [4/4] Locating generated APK...
set "APKFILE="
for /r "%ANDROIDBIN%" %%F in (*-Signed.apk) do set "APKFILE=%%F"
if not defined APKFILE for /r "%ANDROIDBIN%" %%F in (*-signed.apk) do set "APKFILE=%%F"
if not defined APKFILE for /r "%ANDROIDBIN%" %%F in (*.apk) do set "APKFILE=%%F"

if not defined APKFILE (
    echo [ERROR] Build succeeded but no APK was found under:
    echo %ANDROIDBIN%
    echo.
    dir /s /b "%PROJECTDIR%\*.apk" 2>nul
    goto :failed
)

copy /y "!APKFILE!" "%FINALAPK%" >nul
if errorlevel 1 goto :failed

echo.
echo ============================================================
echo   SUCCESS
echo ============================================================
echo APK created:
echo %FINALAPK%
echo.
explorer /select,"%FINALAPK%" >nul 2>&1
pause
exit /b 0

:no_dotnet
echo [ERROR] dotnet was not found. Install Visual Studio with .NET MAUI and .NET 10.
goto :failed

:missing_project
echo [ERROR] Project not found: %PROJECT%
goto :failed

:missing_manifest
echo [ERROR] AndroidManifest not found: %MANIFEST%
goto :failed

:failed
echo.
echo ============================================================
echo   BUILD FAILED
echo ============================================================
echo Read the first error above.
pause
exit /b 1
