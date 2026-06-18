@echo off
setlocal enabledelayedexpansion
title P99 GUI Launcher

echo Checking prerequisites...

python --version >nul 2>&1
if %errorlevel% equ 0 goto :dependencies

echo Python not found. Installing via winget...
winget install --id Python.Python.3.11 -e --silent --accept-source-agreements --accept-package-agreements >nul 2>&1
if %errorlevel% equ 0 goto :path_refresh

echo Winget failed. Downloading Python installer...
curl -L -o python_installer.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
del python_installer.exe

:path_refresh
set "PATH=%PATH%;%USERPROFILE%\AppData\Local\Programs\Python\Python311;%USERPROFILE%\AppData\Local\Programs\Python\Python311\Scripts;%ProgramFiles%\Python311;%ProgramFiles%\Python311\Scripts"

:dependencies
echo Updating pip and installing customtkinter...
python -m pip install --upgrade pip --quiet
python -m pip install customtkinter --quiet

echo Launching GUI...
python gui_wrapper.py
if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)