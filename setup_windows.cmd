@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python no aparece en PATH. Instala Python 3.11 o 3.12 y marca Add Python to PATH.
  pause
  exit /b 1
)
if not exist .venv\Scripts\python.exe python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
if errorlevel 1 (
  echo ERROR al instalar dependencias.
  pause
  exit /b 1
)
echo Instalacion completada. Ejecuta start_windows.cmd para abrir la API.
pause
