@echo off
title OptiCore Suite
cd /d "%~dp0"

:: Verificar si se ejecuta como Administrador
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Ejecutando con permisos de Administrador.
) else (
    echo [AVISO] Solicitando permisos de Administrador para optimizar y reparar...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Localizar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    ) else (
        echo [ERROR] No se encontro Python en el sistema.
        pause
        exit /b
    )
) else (
    set "PYTHON_EXE=python"
)

echo Iniciando OptiCore Suite...
"%PYTHON_EXE%" main.py
pause
