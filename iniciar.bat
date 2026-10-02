@echo off
setlocal enabledelayedexpansion
title OptiCore Suite
cd /d "%~dp0"

:: 1. Verificar si se ejecuta con permisos de Administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [AVISO] Solicitando permisos de Administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: 2. Si ya existe el ejecutable portable compilado, ejecutarlo directamente
if exist "dist\OptiCore.exe" (
    echo [OK] Iniciando ejecutable portable OptiCore.exe...
    start "" "dist\OptiCore.exe"
    exit /b
)

:: 3. Localizar Python universalmente en el sistema
set "PYTHON_CMD="
for %%P in (python.exe py.exe) do (
    where %%P >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=%%P"
        goto :python_found
    )
)

for %%D in (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Python312\python.exe"
) do (
    if exist %%D (
        set "PYTHON_CMD=%%~D"
        goto :python_found
    )
)

:python_found
if "%PYTHON_CMD%"=="" (
    echo [AVISO] No se detecto Python instalado en este computador.
    echo Intentando instalar Python 3.12 automaticamente via Winget...
    winget install Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements --silent
    set "PYTHON_CMD=python"
)

:: 4. Verificar e instalar librerias requeridas si faltan
"%PYTHON_CMD%" -c "import customtkinter, psutil, PIL, requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Instalando dependencias necesarias (customtkinter, psutil, pillow, requests)...
    "%PYTHON_CMD%" -m pip install -r requirements.txt
)

:: 5. Iniciar la aplicacion desde codigo fuente
echo [OK] Iniciando OptiCore Suite...
"%PYTHON_CMD%" main.py
