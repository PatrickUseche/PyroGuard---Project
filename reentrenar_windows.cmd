@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\activate.bat (
  echo Primero ejecuta setup_windows.cmd
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
python scripts\1_generar_dataset.py
if errorlevel 1 goto error
python scripts\2_entrenar_modelo.py
if errorlevel 1 goto error
python -m pytest -q
pause
exit /b 0
:error
echo Hubo un error. Revisa los mensajes anteriores.
pause
exit /b 1
