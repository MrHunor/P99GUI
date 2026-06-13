@echo off
SETLOCAL EnableDelayedExpansion

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to system PATH variables.
    pause
    exit /b
)

:: Auto-install dependencies using the exact Python executable
echo Checking and installing UI dependencies...
python -m pip install customtkinter

:: Run the GUI Wrapper
echo.
echo Launching Steganography Studio...
python "%~dp0gui_wrapper.py"

if %errorlevel% neq 0 (
    echo.
    echo Script crashed or exited with an error. 
    pause
)
ENDLOCAL