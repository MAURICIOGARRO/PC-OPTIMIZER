@echo off
setlocal enabledelayedexpansion
title Compilador de OptiCore a Ejecutable (.EXE)
cd /d "%~dp0"

echo ========================================================
echo       OPTICORE SUITE // GENERADOR DE EJECUTABLE PORTABLE
echo ========================================================
echo.

:: 1. Verificar si Python esta disponible
set "PYTHON_CMD="
for %%P in (python.exe py.exe) do (
    where %%P >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=%%P"
        goto :python_ready
    )
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto :python_ready
)

echo [ERROR] No se encontro Python en el sistema para compilar.
pause
exit /b 1

:python_ready
echo [1/3] Verificando e instalando PyInstaller y librerias...
"%PYTHON_CMD%" -m pip install --upgrade pyinstaller -r requirements.txt

echo.
echo [2/3] Compilando OptiCore.exe portable (un solo archivo con permisos Admin)...
"%PYTHON_CMD%" -m PyInstaller --noconfirm --onefile --windowed --uac-admin --name "OptiCore" --collect-all customtkinter main.py

if %errorlevel% neq 0 (
    echo [ERROR] Ocurrio un fallo durante la compilacion.
    pause
    exit /b 1
)

echo.
echo [3/3] ¡Compilacion completada con exito!
echo.
echo ========================================================
echo El ejecutable portable listo para usar en CUALQUIER PC:
echo Carpeta: dist\OptiCore.exe
echo ========================================================
echo.
pause
