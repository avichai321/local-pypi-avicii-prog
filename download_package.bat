@echo off

rem Check if python is available
where python >nul 2>nul
if %errorlevel% equ 0 (
    python download_packages.py
    goto end
)

where python3 >nul 2>nul
if %errorlevel% equ 0 (
    python3 download_packages.py
    goto end
)

echo Error: Python is not installed. Please install Python to run this script.
exit /b 1

:end
pause