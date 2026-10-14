@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo PyroGuard - Demo del avance de Inteligencia Artificial
echo ============================================
echo.

python ai\1_generar_dataset.py
if errorlevel 1 goto error

echo.
python ai\2_entrenar_modelo.py
if errorlevel 1 goto error

echo.
python ai\3_evaluar_modelo.py
if errorlevel 1 goto error

echo.
echo ============================================
echo Avance ejecutado correctamente.
echo ============================================
pause
exit /b 0

:error
echo.
echo Ocurrio un error. Revisa la salida anterior.
pause
exit /b 1
