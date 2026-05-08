@echo off
chcp 65001 >nul
title IT Tools - Compilador EXE
color 0B
echo.
echo  IT Tools - Compilar a EXE (con UAC Admin)
echo  =============================================
echo.
echo [1/3] Instalando PyInstaller...
python -m pip install pyinstaller --quiet --upgrade
if errorlevel 1 (echo ERROR: Python no encontrado & pause & exit /b 1)
echo.
echo [2/3] Compilando EXE con icono y permisos de Administrador...
python -m PyInstaller --onefile --windowed --uac-admin --manifest admin.manifest --icon ittools.ico --name "IT-Tools" ittools.py
if errorlevel 1 (echo ERROR en la compilacion & pause & exit /b 1)
echo.
echo [3/3] Compilacion completada!
echo El EXE esta en: dist\IT-Tools.exe
echo (El EXE pedira permisos de Admin al ejecutarse)
echo.
explorer dist
pause
